# MAS Mesh (Network) with DIAL

In this task you will practice with MAS (Multi-Agent Systems) Mesh Architecture and develop:
- **Calculations Agent**: has calculator and Python Code Interpreter as tools and can directly communicate with Content Management and WEB Search Agents 
- **Content Management Agent**: able to extract files content and make RAG Search through files content. Can directly communicate with Calculations and WEB Search Agents
- **WEB Search Agent**: has WEB Search capabilities and can directly communicate with Content Management and Calculations Agents

<img src="flow.png">


## Task: 
1. Prepare [core config](core/config.json):
   - Add gpt-4o model 
    ```json
    {
      "gpt-4o": {
        "displayName": "GPT 4o",
        "endpoint": "http://adapter-dial:5000/openai/deployments/gpt-4o/chat/completions",
        "iconUrl": "http://localhost:3001/gpt4.svg",
        "type": "chat",
        "upstreams": [
          {
            "endpoint": "https://ai-proxy.lab.epam.com/openai/deployments/gpt-4o/chat/completions",
            "key": "{YOUR_DIAL_API_KEY}"
          }
        ]
      }
    }
    ```
   - Add Calculations Agent application configuration:
    ```json
    {
      "calculations-agent": {
        "displayName": "Calculations Agent",
        "description": "Calculations Agent. Primary goal to to work with calculations. Capable to make plotly graphics and chart bars. Equipped with: Python Code Interpreter (via MCP), and Simple calculator.",
        "endpoint": "http://host.docker.internal:5001/openai/deployments/calculations-agent/chat/completions",
        "inputAttachmentTypes": [
          "application/pdf",
          "text/html",
          "text/plain",
          "text/csv"
        ],
        "forwardAuthToken": true
      }
    }
    ```
   - Add Content Management Agent application configuration:
    ```json
    {
      "content-management-agent": {
        "displayName": "Content Management Agent",
        "description": "Content Management Agent. Equipped with: Files content extractor and RAG search (supports PDF, TXT, CSV files).",
        "endpoint": "http://host.docker.internal:5002/openai/deployments/content-management-agent/chat/completions",
        "inputAttachmentTypes": [
          "application/pdf",
          "text/html",
          "text/plain",
          "text/csv"
        ],
        "forwardAuthToken": true
      }
    }
    ```
   - Add WEB Search Agent application configuration:
    ```json
    {
      "web-search-agent": {
        "displayName": "WEB Search Agent",
        "description": "WEB Search Agent. Performs research in WEB based on the user request. Equipped with: WEB search (DuckDuckGo via MCP) and is able to fetch WEB pages content.",
        "endpoint": "http://host.docker.internal:5003/openai/deployments/web-search-agent/chat/completions",
        "inputAttachmentTypes": [
          "application/pdf",
          "text/html",
          "text/plain",
          "text/csv"
        ],
        "forwardAuthToken": true
      }
    }
    ```
    **Note: Don't forget to provide model with your DIAL API Key**
2. Run [docker-compose](docker-compose.yml)
3. Check that model is available through the DIAL Chat 👉 http://localhost:3000/
4. Implement all TODOs in:
   - [base_agent_tool.py](task/tools/deployment/base_agent_tool.py)
   - [calculations_agent_tool.py](task/tools/deployment/calculations_agent_tool.py)
   - [content_management_agent_tool.py](task/tools/deployment/content_management_agent_tool.py)
   - [web_search_agent_tool.py](task/tools/deployment/web_search_agent_tool.py)
   - [base_agent.py](task/agents/base_agent.py)
   - [calculations_agent.py](task/agents/calculations/calculations_agent.py)
   - [calculations_app.py](task/agents/calculations/calculations_app.py)
   - [content_management_agent.py](task/agents/content_management/content_management_agent.py)
   - [content_management_app.py](task/agents/content_management/content_management_app.py)
   - [web_search_agent.py](task/agents/web_search/web_search_agent.py)
   - [web_search_app.py](task/agents/web_search/web_search_app.py)
5. Run the applications and test them:
   - Call from Calculations Agent: `I need a chart bar with weather forecast in Kyiv for the next 7 days`. Expected result: call web search agent, then based on the result will generate chart bar with forecasts
   - Call from Calculations Agent: `I need top 3 questions about Java memory model with answers` + [pdf with questions](tests/java-questions-150.pdf)


### Sample of Assistant message State structure with histories:
```json
{
  "state": {
    "tool_call_history": {

    },
    "web_search_agent": {
      "tool_call_history": [
        {

        }
      ]
    },
    "content_management_agent": {
      "tool_call_history": [
        {

        }
      ]
    },
    "calculations_agent": {
      "tool_call_history": [
        {

        }
      ]
    }
  }
}
```
