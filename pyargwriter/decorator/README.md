# Naming Scheme Decorator

- decorator: `add_<func-name>` for example: `add_hydra`
- code generator class: `<func-name>DecoratorWrapGenerator` but with an upper first character. For example: `HydraDecoratorWrapGenerator`
- execute wrapper func: `<func-name>_wrapper`. For example: `hydra_wrapper`

An example how this could work can be viewed with the hydra integration.  
Feel free to explore and add your own options. 