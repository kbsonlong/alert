#!/bin/bash

# 创建告警记录1 - CPU使用率告警（待处理）
curl -X POST "http://localhost:8000/api/alert-records/" \
  -H "Content-Type: application/json" \
  -d '{
    "alert_rule_id": 1,
    "status": "pending",
    "severity": 2,
    "description": "CPU使用率超过80%，当前值为85%",
    "source": "server-01",
    "target": "system.cpu.usage"
  }'

# 创建告警记录2 - 内存使用率告警（处理中）
curl -X POST "http://localhost:8000/api/alert-records/" \
  -H "Content-Type: application/json" \
  -d '{
    "alert_rule_id": 2,
    "status": "processing",
    "severity": 2,
    "description": "内存使用率超过85%，当前值为88%",
    "source": "server-02",
    "target": "system.memory.usage",
    "handled_by": "zhangsan"
  }'

# 创建告警记录3 - 磁盘空间告警（已解决）
curl -X POST "http://localhost:8000/api/alert-records/" \
  -H "Content-Type: application/json" \
  -d '{
    "alert_rule_id": 3,
    "status": "resolved",
    "severity": 3,
    "description": "磁盘空间使用率超过90%，当前值为92%",
    "source": "server-03",
    "target": "system.disk.usage",
    "resolution_note": "已清理临时文件，释放空间",
    "handled_by": "lisi"
  }'

# 创建告警记录4 - CPU使用率告警（已关闭）
curl -X POST "http://localhost:8000/api/alert-records/" \
  -H "Content-Type: application/json" \
  -d '{
    "alert_rule_id": 1,
    "status": "closed",
    "severity": 2,
    "description": "CPU使用率超过80%，当前值为83%",
    "source": "server-04",
    "target": "system.cpu.usage",
    "resolution_note": "系统负载已恢复正常",
    "handled_by": "wangwu"
  }'

# 创建告警记录5 - 内存使用率告警（待处理）
curl -X POST "http://localhost:8000/api/alert-records/" \
  -H "Content-Type: application/json" \
  -d '{
    "alert_rule_id": 2,
    "status": "pending",
    "severity": 2,
    "description": "内存使用率超过85%，当前值为87%",
    "source": "server-05",
    "target": "system.memory.usage"
  }'

# 创建告警记录6 - 磁盘空间告警（处理中）
curl -X POST "http://localhost:8000/api/alert-records/" \
  -H "Content-Type: application/json" \
  -d '{
    "alert_rule_id": 3,
    "status": "processing",
    "severity": 3,
    "description": "磁盘空间使用率超过90%，当前值为95%",
    "source": "server-06",
    "target": "system.disk.usage",
    "handled_by": "zhaoliu"
  }'

# 创建告警记录7 - CPU使用率告警（已解决）
curl -X POST "http://localhost:8000/api/alert-records/" \
  -H "Content-Type: application/json" \
  -d '{
    "alert_rule_id": 1,
    "status": "resolved",
    "severity": 2,
    "description": "CPU使用率超过80%，当前值为82%",
    "source": "server-07",
    "target": "system.cpu.usage",
    "resolution_note": "已重启异常进程",
    "handled_by": "zhangsan"
  }'

# 创建告警记录8 - 内存使用率告警（已关闭）
curl -X POST "http://localhost:8000/api/alert-records/" \
  -H "Content-Type: application/json" \
  -d '{
    "alert_rule_id": 2,
    "status": "closed",
    "severity": 2,
    "description": "内存使用率超过85%，当前值为86%",
    "source": "server-08",
    "target": "system.memory.usage",
    "resolution_note": "已优化内存使用",
    "handled_by": "lisi"
  }'

# 创建告警记录9 - 磁盘空间告警（待处理）
curl -X POST "http://localhost:8000/api/alert-records/" \
  -H "Content-Type: application/json" \
  -d '{
    "alert_rule_id": 3,
    "status": "pending",
    "severity": 3,
    "description": "磁盘空间使用率超过90%，当前值为91%",
    "source": "server-09",
    "target": "system.disk.usage"
  }'

# 创建告警记录10 - CPU使用率告警（处理中）
curl -X POST "http://localhost:8000/api/alert-records/" \
  -H "Content-Type: application/json" \
  -d '{
    "alert_rule_id": 1,
    "status": "processing",
    "severity": 2,
    "description": "CPU使用率超过80%，当前值为84%",
    "source": "server-10",
    "target": "system.cpu.usage",
    "handled_by": "wangwu"
  }'