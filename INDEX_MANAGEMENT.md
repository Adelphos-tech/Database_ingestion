# 🗂️ Index Management

## Executive Summary
Atlas IQ lets you spin up and manage multiple Pinecone indexes directly from the web console. Use indexes for hard isolation (per client or environment) and namespaces (projects) for lightweight separation inside each index.

> **When to create a brand-new index**  
> - You need contractual or compliance isolation.  
> - You want a dedicated environment (prod vs. dev).  
> - You are hitting vector limits and need to shard your corpus.

---

## Concepts at a Glance

| Term | Think of it as | Typical Examples | Notes |
| --- | --- | --- | --- |
| **Index** | Separate database | `client-a-kb`, `prod-knowledge-base`, `archive-2024` | Lives in Pinecone, costs per index, total isolation |
| **Namespace** (Project) | Folder inside an index | `mubest`, `fortius`, `sales` | Cheap subdivision; use first before adding indexes |

```
Index: company-kb
├── Namespace: mubest
│   └── Contracts, reports, pricing sheets
└── Namespace: fortius
    └── Specs, manuals, SOPs
```

---

## Operator Playbook

### 1. Review current indexes
1. Navigate to **🗂️ Indexes** in the sidebar.
2. The dashboard lists every Pinecone index detected via API.
3. `document-knowledge-base` ships as the protected default and cannot be deleted.

### 2. Create a new index
1. From the **🗂️ Indexes** view, enter a name that follows the rules below.
2. Click **Create Index**. Provisioning takes ~30–60 seconds.
3. Once ready, the index appears across all dropdown selectors (Upload, Browse, Chat).

### 3. Work with your index
- **Upload:** Pick an index, then choose the namespace (e.g., Mubest/Fortius) before dragging files.
- **Search / Chat:** Choose index + namespace to query.
- **Browse:** Filter the document list by index + namespace combination.

### 4. Retire an index
1. In **🗂️ Indexes**, select **🗑️ Delete** beside the target index.  
2. Confirm the warning.  
3. Deletion is immediate and irreversible—every vector inside that index is removed.

> ⚠️ **Safety tip:** Export or snapshot vectors before deleting an index. There is no recycle bin.

---

## Use Case Patterns

| Scenario | Suggested Index Strategy |
| --- | --- |
| Multiple clients or business units | `client-a-kb`, `client-b-kb`, `internal-kb` |
| Split by content type | `legal-docs`, `technical-docs`, `marketing-content` |
| Environment separation | `prod-knowledge-base`, `dev-knowledge-base`, `test-knowledge-base` |
| Time-based archives | `archive-2023`, `archive-2024`, `current-documents` |

---

## Technical Reference

### Provisioning defaults
- **Embedding dimension:** 768 (Gemini `text-embedding-004`)
- **Metric:** Cosine similarity
- **Cloud:** AWS (serverless)
- **Region:** `us-east-1` by default (configurable)

### API surface
```http
GET    /api/indexes                # list indexes
POST   /api/indexes               { "index_name": "my-new-index" }
DELETE /api/indexes/{index_name}  # drop index
```

### Naming rules
- Allowed: lowercase letters, numbers, hyphen `-`, underscore `_`
- Avoid uppercase, spaces, punctuation (`!`, `.`, etc.)

Examples:
- ✅ `customer-support`, `legal_docs`, `kb-2024`, `research-papers-v2`
- ❌ `Customer Support`, `KB-2024!`, `Legal.Docs`, `KB_2024_ARCHIVE`

---

## Cost & Capacity Planning

| Plan | Included indexes | Notes |
| --- | --- | --- |
| Pinecone serverless (free) | 1 index | Perfect for pilots; use namespaces for early segmentation |
| Paid tiers | Multiple indexes | ~$0.096/hour (~$70/month) per active index |

**Cost-saving tip:** Start with namespaces inside a single index. Move to multiple indexes only when isolation or scale requires it.

---

## Benefits at a Glance

- ✅ **Isolation:** Perfect for client-level compliance or secret projects  
- ✅ **Organization:** Keep corpora tidy and purposeful  
- ✅ **Security:** Separate retention policies per index  
- ✅ **Performance:** Smaller indexes respond faster  
- ✅ **Flexibility:** Self-service create/delete from the UI

---

## Best Practices Checklist

- [ ] Default to namespaces (projects) for lightweight separation.  
- [ ] Document your naming convention (`client-purpose-environment`).  
- [ ] Monitor index usage; archive or delete dormant ones.  
- [ ] Reuse index + namespace combinations for automation (workflows, integrations).  
- [ ] Back up critical vectors before retiring an index.
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
