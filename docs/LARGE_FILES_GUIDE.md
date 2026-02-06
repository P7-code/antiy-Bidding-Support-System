# 大文件处理和知识库管理指南

## 问题说明

如果您遇到类似以下错误：
```
文件总大小 67.98M，已超过最大限制 20.00M
```

这通常是**开发环境或代码托管平台**的限制，而非项目本身的限制。

## 可能的来源

### 1. 在线开发环境限制
某些在线 IDE（如 Replit、CodeSandbox、Gitpod 等）对工作空间有文件大小限制。

### 2. Git LFS 限制
如果使用 Git LFS 管理大文件，可能有免费额度限制。

### 3. 代码编辑器限制
某些代码编辑器插件或扩展对单文件或总文件大小有限制。

## 解决方案

### 方案 1：使用 Git LFS 管理大文件

如果您的知识库文件较大（超过 10MB），建议使用 Git LFS：

#### 步骤 1：安装 Git LFS
```bash
# macOS
brew install git-lfs

# Linux
sudo apt-get install git-lfs

# Windows
# 下载并安装：https://git-lfs.github.com/
```

#### 步骤 2：初始化 Git LFS
```bash
git lfs install
```

#### 步骤 3：配置追踪大文件
```bash
# 追踪所有 PDF 文件
git lfs track "*.pdf"

# 追踪所有 Word 文档
git lfs track "*.docx"

# 追踪所有 PPT 文件
git lfs track "*.pptx"

# 追踪特定目录中的所有文件
git lfs track "datafiles/**/*"
git lfs track "assets/knowledge_base/**/*"
```

#### 步骤 4：提交 .gitattributes
```bash
git add .gitattributes
git commit -m "chore: 配置 Git LFS"
```

#### 步骤 5：添加大文件
```bash
# 将大文件添加到知识库
git add datafiles/
git commit -m "docs: 添加知识库文件"
git push
```

### 方案 2：使用外部对象存储

如果知识库文件非常大（超过 100MB），建议使用外部对象存储：

#### 使用云存储服务
- **阿里云 OSS**
- **腾讯云 COS**
- **AWS S3**
- **MinIO**（自建）

#### 配置方式
```bash
# 1. 上传文件到云存储
# 2. 在应用中配置访问路径

# 示例：在 .env 中配置
KNOWLEDGE_BASE_URL=https://your-bucket.oss-cn-beijing.aliyuncs.com/
KNOWLEDGE_BASE_ACCESS_KEY=your-access-key
KNOWLEDGE_BASE_SECRET=your-secret-key
```

### 方案 3：压缩知识库文件

如果知识库文件主要是文本，可以压缩后再上传：

```bash
# 压缩知识库目录
tar -czf knowledge_base.tar.gz assets/knowledge_base/

# 解压缩
tar -xzf knowledge_base.tar.gz
```

### 方案 4：分批上传

将知识库文件分批上传：

```bash
# 第一批
git add assets/knowledge_base/商务案例/
git commit -m "docs: 添加商务案例（第一批）"
git push

# 第二批
git add assets/knowledge_base/技术方案/
git commit -m "docs: 添加技术方案（第二批）"
git push
```

## datafiles 目录说明

`datafiles` 目录可用于存储用户上传的知识文档。

### 目录结构
```
datafiles/
├── 商务案例/
│   ├── 项目案例1.pdf
│   └── 资质文件.docx
├── 技术方案/
│   ├── 网络安全方案.pdf
│   └── 系统架构.docx
└── 行业标准/
    ├── 等保2.0标准.pdf
    └── 行业规范.docx
```

### 推荐做法

1. **小文件（< 10MB）**：直接提交到 Git
2. **中等文件（10MB - 100MB）**：使用 Git LFS
3. **大文件（> 100MB）**：使用外部对象存储

## 项目配置建议

### 更新 .gitignore
确保大文件不会被误提交：

```gitignore
# Knowledge base files (use Git LFS instead)
assets/knowledge_base/**/*
!assets/knowledge_base/.gitkeep

datafiles/**/*
!datafiles/.gitkeep

# Git LFS
*.lfs
```

### 创建 .gitattributes
```
# Git LFS 配置
*.pdf filter=lfs diff=lfs merge=lfs -text
*.docx filter=lfs diff=lfs merge=lfs -text
*.pptx filter=lfs diff=lfs merge=lfs -text
*.xlsx filter=lfs diff=lfs merge=lfs -text
assets/knowledge_base/**/* filter=lfs diff=lfs merge=lfs -text
datafiles/**/* filter=lfs diff=lfs merge=lfs -text
```

## 常见平台限制

| 平台 | 文件大小限制 | 说明 |
|------|-------------|------|
| **GitHub** | 单文件 100MB | 超过需要 Git LFS |
| **GitLab** | 单文件 100MB | 超过需要 Git LFS |
| **Gitee** | 单文件 50MB | 超过需要 Git LFS |
| **Git LFS** | 免费额度 1GB/月 | 超过需要付费 |
| **阿里云 OSS** | 无限制 | 按使用量付费 |
| **腾讯云 COS** | 无限制 | 按使用量付费 |

## 调试命令

### 检查 Git LFS 状态
```bash
git lfs status
```

### 查看大文件
```bash
# 查看最大的 10 个文件
find . -type f -exec du -h {} + | sort -rh | head -10

# 查看知识库目录大小
du -sh assets/knowledge_base/
du -sh datafiles/
```

### 检查 Git 仓库大小
```bash
du -sh .git/
```

### 查看 Git LFS 使用情况
```bash
git lfs ls-files
```

## 最佳实践

### 1. 知识库组织
- 按主题分类（商务、技术、标准等）
- 使用清晰的文件命名
- 定期清理过期文件

### 2. 文件管理
- 压缩大文件
- 使用增量更新
- 定期备份

### 3. 版本控制
- 重要文件使用版本控制
- 大文件使用 Git LFS
- 超大文件使用云存储

### 4. 权限管理
- 敏感文件加密
- 设置访问权限
- 定期审计

## 常见问题

### Q: 如何迁移现有的大文件到 Git LFS？
A:
```bash
# 1. 安装 Git LFS
git lfs install

# 2. 迁移现有文件
git lfs migrate import --include="*.pdf,*.docx,*.pptx"

# 3. 推送更改
git push origin --all
```

### Q: Git LFS 免费额度用完了怎么办？
A:
- 购买付费额度
- 或使用外部对象存储

### Q: 如何减少知识库文件大小？
A:
- 压缩文件
- 删除重复内容
- 使用更高效的格式（如 PDF 而非 Word）

### Q: datafiles 目录和 assets/knowledge_base 目录有什么区别？
A:
- `assets/knowledge_base` - 项目内置的知识库
- `datafiles` - 用户上传的知识文档

## 相关文档

- [Git LFS 官方文档](https://git-lfs.github.com/)
- [阿里云 OSS 文档](https://help.aliyun.com/product/31815.html)
- [腾讯云 COS 文档](https://cloud.tencent.com/document/product/436)

---

**最后更新**: 2025-02-05
