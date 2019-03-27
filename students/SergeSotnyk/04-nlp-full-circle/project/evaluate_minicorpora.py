from keysum_evaluator import *


def evaluate_minicorpus_sum():
    corpus_reader = read_parallel_corpus_as_sequence(
        path_to_references='minicorpus_sum/refs',
        path_to_new='minicorpus_sum/set1'
    )
    metrics = evaluate_sequence(corpus_reader,
                                process_keywords=False,
                                process_summary=True)
    print(f"'minicorpus_sum' metrix: {metrics}")


if __name__ == "__main__":
    evaluate_minicorpus_sum()
