# Concept guide

Training changes model parameters using data and an objective; inference uses those parameters to produce an output. A transformer processes token representations through attention and other layers, but the M01 attention script shows only a tiny weighted combination. It cannot predict the behavior of a full language model. Likewise, splitting text on spaces is a teaching analogy, not a provider tokenizer.

A context window constrains the combined instructions, retrieved evidence and output budget. Truncating the tail can remove a condition such as “only after approval”; truncating the head can remove the task. Reserve room for the answer and select context deliberately. Embeddings map content into vectors so geometric similarity can be compared; the hand-made vectors here illustrate the arithmetic, not semantic relevance.

**Decision to defend:** Show how two answers can differ because of context selection, sampling or model version without treating either as an application policy guarantee.
