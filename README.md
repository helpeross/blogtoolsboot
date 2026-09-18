# TBblog Tech Blog

A Hugo + PaperMod static blog for IT & consumer electronics content, built to be deployed on **Cloudflare Pages** and ready for **Amazon Associates (Amazon 联盟) review**.

- **Domain:** `https://blog.toolsboot.com/`
- **Theme:** [PaperMod](https://github.com/adityatelange/hugo-PaperMod)
- **Hugo:** v0.166.0 (Extended)

---

## 1. Project structure

```
toolsboot-blog/
├── hugo.toml                    # 站点主配置（站点名/菜单/SEO/搜索/联盟 tag）
├── content/
│   ├── posts/                   # 6 篇英文示例文章（原创指南类）
│   ├── about.md                 # 关于页
│   ├── contact.md               # 联系页
│   ├── privacy-policy.md        # 隐私政策（Amazon 审核必需）
│   ├── affiliate-disclosure.md  # 联盟披露页（FTC 必需）
│   ├── archives.md              # 归档页
│   └── search.md                # 站内搜索页
├── layouts/
│   ├── index.html               # 自定义首页（Hero/统计/评测方法/分类/信任横幅）
│   ├── shortcodes/
│   │   ├── amazon.html          # Amazon 联盟链接短代码
│   │   └── compare.html         # 产品对比表格短代码
│   └── partials/
│       ├── footer.html          # 全宽多列页脚（含 Amazon 披露）
│       ├── extend_head.html     # Inter 字体与 SEO meta
│       └── extend_post_content.html  # 每篇文章自动注入联盟披露
├── assets/css/extended/
│   ├── custom.css               # 炭黑+橙色设计系统（全部页面样式）
│   └── amazon-card.css          # 联盟卡片样式
├── static/                      # favicon 全套（炭黑+橙）+ _headers
└── make-favicon.ps1 / make-ico.py  # 重新生成 favicon 的脚本
```

## 2. Local preview

```powershell
hugo server -D --bind 127.0.0.1 --port 1314
# 浏览器打开 http://localhost:1314/
```

> 提示：本地预览请用 `localhost` 而非 `127.0.0.1` 访问，站内搜索和 favicon 依赖同源（Hugo 开发服务器默认把 baseURL 解析为 localhost）。

## 3. Deploy to Cloudflare Pages

### 方式 A：连接 Git 仓库（推荐，自动构建）

1. 把本目录推送到 GitHub/GitLab（主题目录 `themes/PaperMod` 已包含在项目内，无需 submodule）：
   ```powershell
   git add .
   git commit -m "Initial blog"
   git remote add origin <your-repo-url>
   git push -u origin main
   ```
2. Cloudflare Dashboard → **Workers & Pages → Create → Pages → Connect to Git**，选择该仓库。
3. 构建设置：
   - **Framework preset:** `Hugo`
   - **Build command:** `hugo --gc --minify`
   - **Build output directory:** `public`
   - **Environment variables:** `HUGO_VERSION = 0.166.0`（可选，Cloudflare 已内置较新 Hugo）
4. 保存并部署。

### 方式 B：Wrangler 直传（无 Git）

```powershell
npx wrangler pages deploy public --project-name toolsboot-blog
```

### 绑定自定义域名

1. 确保 `toolsboot.com` 已接入 Cloudflare（或把 `blog` 子域名的 DNS 指向 Cloudflare）。
2. Pages 项目 → **Custom domains → Set up a custom domain** → 输入 `blog.toolsboot.com`，按提示添加 DNS 记录（CNAME → `toolsboot-blog.pages.dev`，开启代理）。
3. 部署后等待 SSL 证书签发，即可通过 `https://blog.toolsboot.com` 访问。

### 缓存与安全头

`static/_headers` 已在构建时复制到 `public/_headers`，Cloudflare Pages 会自动应用：

- 全站：`X-Frame-Options`、`X-Content-Type-Options`、`Referrer-Policy`
- `/assets/*`：`Cache-Control: public, max-age=604800, immutable`

---

## 4. Amazon 联盟链接用法

### 生成联盟链接

1. 登录 Amazon Associates 后台 → **Product Linking → Site Stripe / Product API** 获取产品 **ASIN** 和你的 **tag**（形如 `yourname-20`）。
2. 在文章中用短代码插入：

```markdown
{{< amazon asin="B0XXXXXXXX" name="Product Name" >}}
```

可选参数：

```markdown
{{< amazon asin="B0XXXXXXXX" name="Product Name" store="amazon.com" tag="yourname-20" text="Check price" note="备注" >}}
```

### 全局替换 tag

在 `hugo.toml` 的 `[params]` 中添加（当前短代码默认值）：

```toml
amazonTag = "yourname-20"
```

> 文章中的 `B0XXXXXXXX` 为占位 ASIN，**提交 Amazon 审核前必须替换为真实产品链接**。

### Amazon Associates 审核基本要求（务必逐项完成）

| 事项 | 状态 | 说明 |
|---|---|---|
| 原创内容 ≥ 5–10 篇 | ⚠️ 示例文章需替换/扩写为你的真实体验 | 审核员人工查看内容质量，避免纯 AI 堆砌与抄袭 |
| Privacy Policy 页面 | ✅ 已创建 | 需把 `<your-email@example.com>` 替换为真实邮箱 |
| Affiliate Disclosure 页面 | ✅ 已创建 | FTC + Amazon 要求 |
| Contact / About 页面 | ✅ 已创建 | 替换邮箱、完善真实团队介绍 |
| 真实可访问的域名 | ⏳ 部署后生效 | 用 `blog.toolsboot.com` |
| 文章内真实联盟链接 | ⚠️ 替换 ASIN/tag | 审核时需有可点击的联盟链接 |
| 图片 | ⚠️ 建议补充 | 用自有实拍图或 Amazon 官方产品图（注意版权） |

---

## 5. 内容与 SEO 建议

- 持续发布原创评测/指南（月 4–8 篇），每篇 800–1500 词。
- 使用文章内 `categories` / `tags` 组织内容（已启用分类与标签页）。
- 默认已开启：RSS、Sitemap、robots.txt、Open Graph、JSON-LD、站内搜索。
- 可选：接入 Cloudflare Web Analytics（Pages 控制台一键开启，无需改代码）。

## 6. 常见操作

```powershell
hugo new content posts/your-new-post.md   # 新建文章
hugo --gc --minify                        # 生产构建到 public/
```

---

© 2026 TBblog — As an Amazon Associate, we earn from qualifying purchases.
