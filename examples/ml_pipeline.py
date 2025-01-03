from typing import Any

from omegaconf import DictConfig
from pyargwriter.decorator import add_hydra


class Entrypoint:
    """Entrypoint for a machine learning pipeline.

    This class serves as the main interface for executing different stages of
    a machine learning pipeline, including training, evaluation, and prediction.
    """

    def __init__(self):
        """Initializes the Entrypoint."""

    @add_hydra("train_config", version_base=None, config_name="train_config.yaml")
    def train(self, train_config: DictConfig, device: str = "cpu"):
        """Executes the training process.

        This method is responsible for training the machine learning model
        using the parameters provided in the configuration.

        Args:
            train_config (DictConfig): A path to a     dictionary containing configuration parameters
            device (str): either cpu or cuda

        Note:
            This is a mockup method and does not implement actual training logic.
        """
        print("Training the model with the following configuration:")
        print(train_config, type(train_config))
        print("Start training on: ", device)

    def evaluate(self):
        """Evaluates the model performance.

        This method calculates and reports metrics to assess the quality of the
        trained model on a validation or test dataset.

        Note:
            This is a mockup method and does not implement actual evaluation logic.
        """
        print("Evaluating the model...")

    def predict(self, inputs: list[int]):
        """Generates predictions for given inputs.

        Args:
            inputs (list[int]): Data inputs for which predictions are to be made.

        Returns:
            list: Mockup predictions for the given inputs.

        Note:
            This is a mockup method and does not implement actual prediction logic.
        """
        print(f"Generating predictions for inputs: {inputs}")
        return ["mock_prediction" for _ in inputs]

    def run(self, stage: str, **kwargs):
        """Runs a specific stage of the pipeline.

        Args:
            stage (str): The pipeline stage to execute. Must be one of
                ['train', 'evaluate', 'predict'].
            **kwargs: Additional keyword arguments specific to the chosen stage.

        Raises:
            ValueError: If the provided stage is not supported.
        """
        if stage == "train":
            self.train()
        elif stage == "evaluate":
            self.evaluate()
        elif stage == "predict":
            inputs = kwargs.get("inputs", [])
            return self.predict(inputs)
        else:
            raise ValueError(f"Unsupported pipeline stage: {stage}")
