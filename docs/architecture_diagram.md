'''mermaid

flowchart TD

&#x20;   A\[Razorpay Test Mode / Synthetic Data] --> B\[FastAPI Backend]

&#x20;   B --> C\[Transaction and Customer Database]

&#x20;   C --> D\[Diagnosis Service]

&#x20;   D --> E\[ML Recovery Probability Model]

&#x20;   E --> F\[Expected Recovery Value Engine]

&#x20;   F --> G\[Decision Engine]

&#x20;   G --> H\[Policy and Safety Gate]

&#x20;   H --> I\[Action Executor]

&#x20;   I --> J\[Recovery Outcome]

&#x20;   J --> K\[Audit Trail]

&#x20;   K --> L\[React Dashboard]

&#x20;   G --> M\[LLM Explanation - Gemini, with fallback]

&#x20;   M --> K

