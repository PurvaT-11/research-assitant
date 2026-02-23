AI Research Agent
=================

A minimal but structured AI research agent that:

*   Accepts a research prompt
    
*   Plans investigation angles
    
*   Searches the web
    
*   Extracts structured evidence
    
*   Scores source credibility
    
*   Filters low-quality claims
    
*   Refines search if evidence is weak
    
*   Produces a Markdown research report
    
*   Logs full trace for debugging
    

1\. Overview
------------

This project implements a modular research agent that transforms an open-ended research question into a structured evidence-backed report.

The agent enforces:

*   Claim–evidence separation
    
*   Verbatim snippet validation
    
*   Domain-based credibility scoring
    
*   Confidence weighting
    
*   Deduplication
    
*   Automatic refinement loop
    

It outputs:

*   report.md — Final research report
    
*   trace.json — Full execution trace
    

2\. Architecture
----------------

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   User Question      ↓Guardrails      ↓Planner (LLM)      ↓Search (Tavily API)      ↓Extractor (LLM)      ↓Credibility Engine      ↓Filter + Deduplicate      ↓Refinement (if needed)      ↓Markdown Report + Trace JSON   `

3\. Project Structure
---------------------

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   ai-research-agent/│├── main.py├── agent.py├── planner.py├── search.py├── extractor.py├── credibility.py├── guardrails.py├── report.py├── domain_policy.py├── requirements.txt└── outputs/   `

4\. Key Components
------------------

### 4.1 Guardrails

*   Rejects non-research prompts
    
*   Prevents casual / recipe-style queries
    
*   Enforces investigative framing
    

### 4.2 Planner

Uses OpenAI to:

*   Identify multiple research angles
    
*   Generate structured search queries
    

Output example:

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   {  "queries": [    "synthetic data LLM risks peer reviewed study",    "synthetic data LLM benefits systematic review"  ]}   `

### 4.3 Search Layer

*   Tavily API
    
*   Returns content + URLs
    
*   Limited results for efficiency
    

### 4.4 Extractor

LLM-based extraction that outputs:

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   {  "claims": [    {      "claim": "...",      "evidence_snippet": "...",      "confidence": 0.8    }  ]}   `

Hallucination protection:

*   Evidence snippet must exist verbatim in page content
    

### 4.5 Credibility Engine

Domain-based base credibility:

Domain TypeScoreAcademic (arxiv, nature, acm, ieee)0.85–0.9Government / Policy0.75Industry0.7Blog / Unknown0.5

Enhancements:

*   Agreement bonus (cross-source reinforcement)
    
*   Final credibility cap at 1.0
    
*   Final confidence = model\_confidence × final\_credibility
    

### 4.6 Refinement Loop

If:

*   Fewer than 5 strong claims
    
*   OR average credibility < 0.6
    

Then:

*   Generate refined academic-style queries
    
*   Re-run search
    
*   Re-filter and re-rank
    

5\. Output Format
-----------------

Each claim includes:

*   Claim
    
*   Verbatim evidence snippet
    
*   Source URL
    
*   Base credibility
    
*   Agreement bonus
    
*   Final credibility
    
*   Final confidence
    

6\. Example Run
---------------

Input:

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   What are the risks and benefits of synthetic data for training LLMs?   `

Output:

*   Structured Markdown research report
    
*   Filtered top claims ranked by confidence
    
*   Trace file containing:
    
    *   All queries
        
    *   Search results
        
    *   Raw extracted claims
        
    *   Final ranked claims
        
    *   Average credibility
        

7\. Installation
----------------

### 1️⃣ Create environment

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   python3 -m venv research_envsource research_env/bin/activate   `

### 2️⃣ Install dependencies

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   pip install -r requirements.txt   `

### 3️⃣ Set API keys

Create a .env file:

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   OPENAI_API_KEY=your_openai_keyTAVILY_API_KEY=your_tavily_key   `

8\. Run the Agent
-----------------

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   python main.py   `

Enter a research question when prompted.

Outputs will be saved in:

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   outputs/report.mdoutputs/trace.json   `

9\. Reliability & Safety
------------------------

Implemented safeguards:

*   Research-only prompt validation
    
*   Verbatim snippet verification
    
*   Low-credibility filtering
    
*   Deduplication
    
*   Single refinement retry
    
*   Trace logging for debugging
    

10\. Tradeoffs
--------------

Design ChoiceTradeoffDomain-based credibilitySimple but heuristicSingle refinement passEfficient but not exhaustiveLLM extractionFlexible but slowerContent truncation (2000 chars)Faster but may miss context

11\. Future Extensions
----------------------

With unlimited time, this system could evolve into:

*   Citation graph cross-verification
    
*   Multi-hop reasoning memory
    
*   Embedding-based claim clustering
    
*   Adaptive credibility thresholds per domain
    
*   Async search pipeline
    
*   Self-evaluation scoring model
    
*   Retrieval-augmented reasoning over local corpora
    
*   Automatic contradiction detection
    
*   Evaluation harness for factual accuracy
    

12\. Why This Project Matters
-----------------------------

Most LLM-based research systems:

*   Do not separate claim from evidence
    
*   Do not verify snippet presence
    
*   Do not score source credibility
    
*   Do not log full trace
    

This system enforces structural rigor and transparency.

13\. Author
-----------

Built as a modular research agent prototype exploring structured AI reasoning, credibility scoring, and iterative evidence refinement.