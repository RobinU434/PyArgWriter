import inspect
from argparse import (
    Action,
    ArgumentParser,
    _StoreAction,
    _StoreTrueAction,
    _VersionAction,
    Namespace,
    ArgumentError
)
from textwrap import dedent
from typing import Any, Callable, Dict

from hydra import version
from hydra._internal.deprecation_warning import deprecation_warning
from hydra._internal.utils import _run_hydra, get_args_parser
from hydra.main import _UNSPECIFIED_, _get_rerun_conf
from hydra.core.utils import _flush_loggers



def add_hydra_parser(new_parser: ArgumentParser = None) -> ArgumentParser:
    """_summary_

    Args:
        new_parser (ArgumentParser, optional): _description_. Defaults to None.

    Raises:
        err: _description_
        NotImplementedError: _description_

    Returns:
        ArgumentParser: _description_
    """
    if new_parser is None:
        new_parser = ArgumentParser(add_help=False)

    hydra_parser = get_args_parser()

    for action in hydra_parser._actions:
        action: Action
        option_strings = action.option_strings
            
        if len(option_strings) == 0:
            new_parser.add_argument(
                action.dest,
                nargs=action.nargs,
                help=action.help,
            )
        elif isinstance(action, _StoreAction):
            new_parser.add_argument(
                *option_strings,
                action="store",
                nargs=action.nargs,
                default=action.default,
                type=action.type,
                help=action.help,
                choices=action.choices,
            )
                
        elif isinstance(action, _StoreTrueAction):
            try:            
                new_parser.add_argument(
                    *option_strings,            
                    action="store_true",
                    help=action.help,
                )
            except ArgumentError as err:
                if action.dest == "help":   
                    continue
                raise err
        elif isinstance(action, _VersionAction):
            new_parser.add_argument(
                "--hydra-version",
                action="version",
                help=action.help,
                version=action.version,
            )
        else:
            raise NotImplementedError
    return new_parser


def hydra_wrapper(
    task_func: Callable[[Any], Any],
    cli_args: Dict[str, Any],
    arg_parser: ArgumentParser,
    config_var_name: str = "cfg",
    version_base: str = _UNSPECIFIED_,
    config_path: str = _UNSPECIFIED_,
    config_name: str = None,
):
    """_summary_

    Args:
        task_func (Callable[[Any], Any]): _description_
        cli_args (Dict[str, Any]): _description_
        arg_parser (ArgumentParser): _description_
        config_var_name (str, optional): _description_. Defaults to "cfg".
        version_base (str, optional): _description_. Defaults to _UNSPECIFIED_.
        config_path (str, optional): _description_. Defaults to _UNSPECIFIED_.
        config_name (str, optional): _description_. Defaults to None.
    """
    version.setbase(version_base)

    if config_path is _UNSPECIFIED_:
        if version.base_at_least("1.2"):
            config_path = None
        elif version_base is _UNSPECIFIED_:
            url = "https://hydra.cc/docs/1.2/upgrades/1.0_to_1.1/changes_to_hydra_main_config_path"
            deprecation_warning(
                message=dedent(
                    f"""
                config_path is not specified in @hydra.main().
                See {url} for more information."""
                ),
                stacklevel=2,
            )
            config_path = "."
        else:
            config_path = "."
    
    # TODO: hacky solution: help is being ignored while adding the hydra parser so help is always False
    cli_args["help"] = False
    cli_args = Namespace(**cli_args)  # convert to Namespace

    signature = inspect.signature(task_func, follow_wrapped=True)
    parameters = dict(signature.parameters)
    parameters.pop(config_var_name)
    task_func_args = {k: getattr(cli_args, k) for k in parameters}

    # add default job name as task function name if not provided otherwise
    overrides = {}
    for ele in cli_args.overrides:
        k, v = ele.split("=")
        overrides[k] = v
    job_name_key = "hydra.job.name"
    if job_name_key not in overrides:
        overrides[job_name_key] = task_func.__name__
    cli_args.overrides = [f"{k}={v}" for k, v in overrides.items()]

    
    if cli_args.experimental_rerun is not None:
        cfg = _get_rerun_conf(
            cli_args.experimental_run, cli_args.overrides
        )
        task_func(**{config_var_name: cfg, **task_func_args})
        _flush_loggers()
    else:
        # no return value from run_hydra() as it may sometime actually run the task_function
        # multiple times (--multirun)
        _run_hydra(
            args=cli_args,
            args_parser=arg_parser,
            task_function=lambda config: task_func(
                **{config_var_name: config, **task_func_args}
            ),
            config_path=config_path,
            config_name=config_name,
        )