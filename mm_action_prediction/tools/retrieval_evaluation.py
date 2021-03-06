"""Script evaluates response retrieval using GT responses.

Author(s): Satwik Kottur
"""


from absl import app, flags
import json

import numpy as np


FLAGS = flags.FLAGS
flags.DEFINE_string(
    "retrieval_json_path", "data/furniture_train.json", "Data with gold responses"
)
flags.DEFINE_string(
    "model_score_path", None, "Candidate scores generated by the model"
)


def evaluate_response_retrieval(gt_responses, model_scores):
    """Evaluates response retrieval using the raw data and model predictions.
    """
    # NOTE: Update this later to include gt_index for candidates.
    gt_ranks = []
    for model_datum in model_scores:
        for _round_id, round_datum in enumerate(model_datum["candidate_scores"]):
            gt_score = round_datum[0]
            gt_ranks.append(np.sum(np.array(round_datum) > gt_score) + 1)
    gt_ranks = np.array(gt_ranks)
    return {
        "r1": np.mean(gt_ranks <= 1),
        "r5": np.mean(gt_ranks <= 5),
        "r10": np.mean(gt_ranks <= 10),
        "mean": np.mean(gt_ranks),
        "mrr": np.mean(1 / gt_ranks)
    }


def main(_):
    print("Reading: {}".format(FLAGS.data_json_path))
    with open(FLAGS.data_json_file, "r") as file_id:
        gt_responses = json.load(file_id)
    print("Reading: {}".format(FLAGS.model_output_path))
    with open(FLAGS.model_score_path, "r") as file_id:
        model_scores = json.load(file_id)
    retrieval_metrics = evaluate_response_retrieval(gt_responses, model_scores)
    print(retrieval_metrics)


if __name__ == "__main__":
    app.run(main)
