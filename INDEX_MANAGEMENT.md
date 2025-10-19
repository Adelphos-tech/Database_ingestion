# 🗂️ Index Management Feature

## Overview

You can now create and manage multiple Pinecone indexes directly from the web interface! This allows you to completely separate different knowledge bases.

## What are Indexes?

**Indexes** are separate vector databases in Pinecone. Think of them as different "containers" for your knowledge bases.

### Index vs Project (Namespace)

- **Index**: Completely separate database (e.g., `company-kb`, `customer-support-kb`, `research-papers`)
- **Project (Namespace)**: Subdivision within an index (e.g., `mubest`, `fortius`)

**Example Structure:**
```
Index: company-kb
├── Project: mubest
│   └── Documents: contracts, reports, etc.
└── Project: fortius
    └── Documents: specifications, manuals, etc.

Index: customer-support-kb
├── Project: mubest
│   └── Documents: support tickets, FAQs
└── Project: fortius
    └── Documents: troubleshooting guides
```

## How to Use

### 1. View All Indexes

1. Click the **"🗂️ Indexes"** tab
2. See all your Pinecone indexes
3. Default index: `document-knowledge-base` (protected, cannot be deleted)

### 2. Create New Index

1. Go to **"🗂️ Indexes"** tab
2. Enter a name in the input field
   - Use lowercase letters, numbers, hyphens, underscores only
   - Example: `customer-support`, `research_papers`, `legal-docs`
3. Click **"Create Index"**
4. Wait for creation (takes ~30-60 seconds)
5. New index automatically appears in all dropdowns

### 3. Use Different Indexes

**When Uploading:**
- Select your desired index from the "Select Index" dropdown
- Select your project (Mubest/Fortius)
- Upload documents

**When Searching:**
- Choose the index to search
- Choose the project
- Enter your query

**When Browsing:**
- Select index and project to view documents

### 4. Delete Index

1. Go to **"🗂️ Indexes"** tab
2. Click **"🗑️ Delete"** on any index (except default)
3. Confirm deletion
4. ⚠️ **Warning**: This permanently deletes ALL data in that index!

## Use Cases

### 1. Separate Organizations
```
Index: client-a-kb (Client A's data)
Index: client-b-kb (Client B's data)
Index: internal-kb  (Your company's data)
```

### 2. Separate Content Types
```
Index: legal-documents
Index: technical-docs
Index: marketing-content
```

### 3. Development vs Production
```
Index: prod-knowledge-base
Index: dev-knowledge-base
Index: test-knowledge-base
```

### 4. Time-based Separation
```
Index: archive-2023
Index: archive-2024
Index: current-documents
```

## Technical Details

### Index Configuration
- **Dimension**: 768 (Gemini embedding size)
- **Metric**: Cosine similarity
- **Cloud**: AWS
- **Region**: us-east-1 (configurable in backend)
- **Type**: Serverless

### API Endpoints

**List all indexes:**
```bash
GET /api/indexes
```

**Create new index:**
```bash
POST /api/indexes
Body: { "index_name": "my-new-index" }
```

**Delete index:**
```bash
DELETE /api/indexes/{index_name}
```

### Naming Rules

✅ **Valid names:**
- `customer-support`
- `legal_docs`
- `kb-2024`
- `research-papers-v2`

❌ **Invalid names:**
- `Customer Support` (no spaces)
- `KB-2024!` (no special characters)
- `Legal.Docs` (no periods)
- `KB_2024_ARCHIVE` (no uppercase)

## Cost Considerations

- **Pinecone Free Tier**: 1 serverless index
- **To create multiple indexes**: Upgrade to paid plan
- **Paid Plan**: ~$0.096/hour per index (~$70/month per index)

**Recommendation**: Use namespaces (projects) for organization within the free tier, use multiple indexes only when you need complete data isolation.

## Benefits

✅ **Complete Data Isolation**: Separate clients/departments completely
✅ **Better Organization**: Group related content together
✅ **Security**: Keep sensitive data in separate indexes
✅ **Performance**: Smaller indexes = faster searches
✅ **Flexible**: Easy to create and delete as needed

## Best Practices

1. **Start with Namespaces**: Use projects (Mubest/Fortius) first
2. **Create Indexes for**: Complete separation needs
3. **Naming Convention**: Use descriptive, consistent names
4. **Document Your Structure**: Keep track of what each index contains
5. **Backup Important Data**: Before deleting an index

## FAQ

**Q: How many indexes can I create?**
A: Free tier = 1, Paid tier = unlimited (but costs per index)

**Q: Can I rename an index?**
A: No, you must create a new one and migrate data

**Q: What happens if I delete an index?**
A: All vectors and data are permanently deleted (cannot be recovered)

**Q: How long does it take to create an index?**
A: Usually 30-60 seconds

**Q: Can I have different embedding dimensions per index?**
A: Yes, but this app creates all with dimension 768 (Gemini)

**Q: Should I use indexes or namespaces?**
A: Use namespaces (projects) unless you need complete separation

---

**Ready to organize your knowledge base?** Head to the 🗂️ Indexes tab and start creating!
