# Research —20 October2026

Demand is **inferred**, not a verified request for this tool. A failing inclusion comparison needs a small reproducible sequence and both state traces; a finite test corpus cannot establish language inclusion.

## Observed comparables

Query `finite automata`, GitHub repository search sorted by Most stars: [exact search](https://github.com/search?q=finite+automata&type=repositories&s=stars&o=desc). The highest-star relevant comparable found in this research pool is `rust-lang/regex`; this is not an exhaustive global ranking.

| Repository | Stars observed | Last push | License metadata | Workflow / scope |
| --- | ---: | --- | --- | --- |
| [rust-lang/regex](https://github.com/rust-lang/regex) | 4044 | 2026-10-19T17:59:23Z | Apache-2.0 | Rust regex matching engine; adjacent higher-star alternative, not a direct explicit-DFA inclusion CLI. |
| [caleb531/automata](https://github.com/caleb531/automata) | 412 | 2026-06-25T19:41:27Z | MIT | Python automata library with deterministic/nondeterministic and other machines, diagrams and language operations. |
| [cs-au-dk/dk.brics.automaton](https://github.com/cs-au-dk/dk.brics.automaton) | 248 | 2025-09-14T11:53:41Z | NOASSERTION | Java DFA/NFA library with Unicode alphabet and regular-expression operations. |

## Workflow choice and tradeoffs

Parser/protocol engineers checking that an explicit finite recognizer change preserves accepted token sequences. Explore the finite DFA product to prove left-language inclusion or return a shortest token counterexample with both state traces.

rup-proof-trace checks clause proof steps and spdx-expression-paths enumerates license alternatives. This checks inclusion of finite token languages and produces a counterexample, not SAT or grammar parsing.

This is a bounded dedicated report with an invented fixture and zero runtime dependencies. The established tools are broader; choose them when their ecosystem, formats or capabilities match the job. Our own installed example proves only our documented behavior. Competitor clean installs, time to first useful result, support response times, reliability and equivalent-workload performance were not measured. Current docs offer install/usage guidance; sampled issue activity is preserved as evidence, not a support-quality score. No feature absence or superiority is claimed.

## Coverage and evidence

The keyword search includes irrelevant results (SQL knowledge graphs, CSS critical paths, routing deployment projects and regex engines). Relevant comparables were also found directly; filtering was based on current README scope. [Exact dated metadata and issue samples](RESEARCH_PROVENANCE.json). Own acceptance and distinction: [brief](BRIEF.json). No implementation, branding or prose was copied.
