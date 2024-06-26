# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

from pathlib import Path

from promptflow.client import load_flow
from promptflow.core._prompty_utils import convert_model_configuration_to_connection


class RelevanceEvaluator:
    def __init__(self, model_config):
        """
        Initialize an evaluator configured for a specific Azure OpenAI model.

        :param model_config: Configuration for the Azure OpenAI model.
        :type model_config: AzureOpenAIModelConfiguration

        **Usage**

        .. code-block:: python

            eval_fn = RelevanceEvaluator(model_config)
            result = eval_fn(
                question="What is the capital of Japan?",
                answer="The capital of Japan is Tokyo.",
                context="Tokyo is Japan's capital, known for its blend of traditional culture \
                    and technological advancements.")
        """

        # Load the flow as function
        current_dir = Path(__file__).resolve().parent
        flow_dir = current_dir / "flow"
        self._flow = load_flow(source=flow_dir)

        # Override the connection
        connection = convert_model_configuration_to_connection(model_config)
        self._flow.context.connections = {
            "query_llm": {
                "connection": connection,
                "deployment_name": model_config.azure_deployment,
            }
        }

    def __call__(self, *, question: str, answer: str, context: str, **kwargs):
        """Evaluate relevance.

        :param question: The question to be evaluated.
        :type question: str
        :param answer: The answer to be evaluated.
        :type answer: str
        :param context: The context to be evaluated.
        :type context: str
        :return: The relevance score.
        :rtype: dict
        """

        # Run the evaluation flow
        return self._flow(question=question, answer=answer, context=context)
