# API 参考文档

## 认证

所有API请求需要在Header中携带JWT Token：
```
Authorization: Bearer <your_token>
```

## 告警规则接口

### 获取告警规则列表

```http
GET /api/v1/alert-rules
```

**查询参数：**
- `page`: 页码，默认1
- `size`: 每页数量，默认20
- `enabled`: 是否启用，可选true/false

**响应示例：**
```json
{
  "total": 100,
  "items": [
    {
      "id": 1,
      "name": "CPU使用率告警",
      "target": "system.cpu.usage",
      "condition": ">",
      "threshold": 90,
      "severity": "critical",
      "enabled": true,
      "notification_group_id": 1,
      "notification_template_id": 1
    }
  ]
}
```

### 创建告警规则

```http
POST /api/v1/alert-rules
```

**请求体：**
```json
{
  "name": "CPU使用率告警",
  "target": "system.cpu.usage",
  "condition": ">",
  "threshold": 90,
  "severity": "critical",
  "notification_group_id": 1,
  "notification_template_id": 1
}
```

## 通知渠道接口

### 获取通知渠道列表

```http
GET /api/v1/notification-channels
```

**响应示例：**
```json
{
  "total": 50,
  "items": [
    {
      "id": 1,
      "name": "运维组邮件",
      "type": "email",
      "config": {
        "smtp_host": "smtp.example.com",
        "smtp_port": 587
      },
      "enabled": true
    }
  ]
}
```

### 创建通知渠道

```http
POST /api/v1/notification-channels
```

**请求体：**
```json
{
  "name": "运维组邮件",
  "type": "email",
  "config": {
    "smtp_host": "smtp.example.com",
    "smtp_port": 587,
    "username": "alert@example.com",
    "password": "your-password"
  }
}
```

## 通知组接口

### 获取通知组列表

```http
GET /api/v1/notification-groups
```

**响应示例：**
```json
{
  "total": 20,
  "items": [
    {
      "id": 1,
      "name": "运维团队",
      "members": {
        "members": [
          {
            "name": "张三",
            "email": "zhangsan@example.com",
            "phone": "13800138000"
          }
        ]
      },
      "channels": {
        "channels": [1, 2]
      }
    }
  ]
}
```

### 创建通知组

```http
POST /api/v1/notification-groups
```

**请求体：**
```json
{
  "name": "运维团队",
  "members": {
    "members": [
      {
        "name": "张三",
        "email": "zhangsan@example.com",
        "phone": "13800138000"
      }
    ]
  },
  "channels": {
    "channels": [1, 2]
  }
}
```

## 通知模板接口

### 获取通知模板列表

```http
GET /api/v1/notification-templates
```

**响应示例：**
```json
{
  "total": 30,
  "items": [
    {
      "id": 1,
      "name": "默认邮件模板",
      "type": "email",
      "content": "告警: {{alert_name}}\n触发时间: {{trigger_time}}\n详情: {{details}}",
      "variables": {
        "variables": ["alert_name", "trigger_time", "details"]
      },
      "language": "zh-CN"
    }
  ]
}
```

### 创建通知模板

```http
POST /api/v1/notification-templates
```

**请求体：**
```json
{
  "name": "默认邮件模板",
  "type": "email",
  "content": "告警: {{alert_name}}\n触发时间: {{trigger_time}}\n详情: {{details}}",
  "variables": {
    "variables": ["alert_name", "trigger_time", "details"]
  },
  "language": "zh-CN"
}
```

## 告警历史接口

### 获取告警历史列表

```http
GET /api/v1/alert-history
```

**查询参数：**
- `page`: 页码，默认1
- `size`: 每页数量，默认20
- `start_time`: 开始时间，ISO8601格式
- `end_time`: 结束时间，ISO8601格式
- `severity`: 告警级别

**响应示例：**
```json
{
  "total": 1000,
  "items": [
    {
      "id": 1,
      "alert_rule_id": 1,
      "alert_name": "CPU使用率告警",
      "trigger_time": "2024-01-20T10:30:00Z",
      "severity": "critical",
      "status": "resolved",
      "resolve_time": "2024-01-20T10:35:00Z",
      "details": "CPU使用率达到95%"
    }
  ]
}
```