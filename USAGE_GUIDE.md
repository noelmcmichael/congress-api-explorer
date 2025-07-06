# 📖 Congress API Explorer - Common Usage Guide

## 🚀 **How to Start Using It**

### Quick Start
1. **Start the MCP Server**:
   ```bash
   cd /Users/noelmcmichael/Workspace/congress_api_explorer
   uv run scripts/run_mcp_server.py
   ```

2. **Connect from Memex**: The server will be available as "congress-api-explorer"

3. **Start asking questions** about US Congressional data!

## 💬 **Common Usage Patterns**

### 🏛️ **Committee Information**
Ask natural language questions like:

**"What committees are in the House of Representatives?"**
- Uses: `get_committees` tool
- Returns: List of House committees with details

**"Tell me about the House Agriculture Committee"**  
- Uses: `get_committee_details` tool
- Returns: Detailed committee information

**"What hearings has the House Agriculture Committee held?"**
- Uses: `get_committee_hearings` tool  
- Returns: Recent committee hearings and meetings

### 📋 **Congressional Bills**
**"Show me recent bills in Congress"**
- Uses: `get_bills` tool
- Returns: Latest bills with titles and actions

**"What's the status of HR 1?"**
- Uses: `get_bill_details` tool
- Returns: Detailed bill information, sponsor, actions

**"Search for infrastructure bills"**
- Uses: `search_bills` tool
- Returns: Bills matching "infrastructure" keyword

### 👥 **Congressional Members**
**"Who are the current House members?"**
- Uses: `get_members` tool
- Returns: List of current House representatives

**"Tell me about Nancy Pelosi"**
- Uses: `get_member_details` tool (with bioguide ID)
- Returns: Detailed member information

### 🔍 **Cross-Data Search**
**"Search for anything related to healthcare"**
- Uses: `search_all` tool
- Returns: Healthcare-related bills, hearings, committees, members

**"Find all defense-related congressional activity"**
- Uses: `search_by_topic` tool with topic="defense"
- Returns: Defense-related data across all types

### 📊 **System Status & Monitoring**
**"What's the system health status?"**
- Uses: `get_health_status` tool
- Returns: Comprehensive system health report

**"Show me API usage statistics"**
- Uses: `get_rate_limit_status` tool
- Returns: Current API usage and remaining limits

## 🎯 **Practical Examples**

### Example 1: Committee Research
```
You: "What committees is Alexandria Ocasio-Cortez on?"

System will:
1. Search for AOC in members
2. Find her committee assignments
3. Return committee details with her roles
```

### Example 2: Bill Tracking
```
You: "What's happening with climate change legislation?"

System will:
1. Search bills for "climate change"
2. Find related hearings
3. Show committee activity
4. Return comprehensive climate legislation status
```

### Example 3: Hearing Investigation
```
You: "What hearings are scheduled about the budget?"

System will:
1. Search hearings for "budget"
2. Find relevant committees
3. Show recent and upcoming budget hearings
4. Include witness information if available
```

### Example 4: Cross-Reference Analysis
```
You: "Show me everything Congress is doing about infrastructure"

System will:
1. Search all data types for "infrastructure"
2. Find related bills, hearings, committees
3. Cross-reference member involvement
4. Provide comprehensive infrastructure overview
```

## ⚡ **Power User Tips**

### 1. **Specific Searches Work Better**
- ❌ "Tell me about Congress"
- ✅ "Show me House Agriculture Committee hearings from this year"

### 2. **Use Topic Categories**
Available topics: healthcare, economy, defense, education, environment, immigration, infrastructure, energy, finance, agriculture, technology, transportation

### 3. **Combine Multiple Queries**
- "What bills has the House passed about infrastructure, and which committees handled them?"

### 4. **Check System Performance**
- "What's the API usage status?" - To see if you're hitting rate limits
- "Show system health" - To check overall system performance

### 5. **Use Current Congress Numbers**
- Current Congress is 119 (2025-2026)
- Specify congress numbers for historical data

## 🔧 **Available Tools Reference**

| Tool Category | Tools | What They Do |
|---------------|-------|--------------|
| **Committees** | `get_committees`, `get_committee_details`, `get_committee_hearings` | Committee information and activities |
| **Hearings** | `get_hearings`, `search_hearings` | Congressional hearings and meetings |
| **Bills** | `get_bills`, `get_bill_details`, `search_bills` | Legislation tracking and details |
| **Members** | `get_members`, `get_member_details` | Congressional member information |
| **Search** | `search_all`, `search_by_topic` | Cross-data search capabilities |
| **Utility** | `get_congress_info`, `get_rate_limit_status` | System information |
| **Health** | `get_health_status`, `get_system_metrics` | System monitoring |

## 🎭 **Real-World Use Cases**

### **Journalist Research**
- "What hearings are happening about tech regulation?"
- "Which members sponsored recent privacy bills?"
- "Show me all Congressional activity on social media legislation"

### **Citizen Engagement**
- "What's my representative working on?"
- "What bills are being voted on this week?"
- "Which committees are discussing climate change?"

### **Academic Research**
- "Compare healthcare bills from different committees"
- "Track infrastructure spending legislation over time"
- "Analyze committee hearing patterns on specific topics"

### **Policy Analysis**
- "What's the status of all immigration bills?"
- "Which committees have the most hearings on economic policy?"
- "Show me cross-party cooperation on specific issues"

## 🛟 **Troubleshooting**

### If queries aren't working:
1. **Check system health**: "What's the system health status?"
2. **Check API limits**: "Show me API usage statistics"
3. **Try simpler queries**: Start with basic committee or bill searches
4. **Use specific terms**: Instead of "politics" try "healthcare bills"

### Performance optimization:
- The system caches responses for faster repeated queries
- API usage is tracked and limited to stay within Congress API limits
- Health monitoring provides real-time system status

---

🎉 **You're ready to explore US Congressional data with natural language queries!**

Start with simple questions and build up to more complex cross-referenced searches.