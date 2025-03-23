from sqlalchemy.orm import Session
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import SessionLocal
from models.alert_rule_model import AlertRule
from models.notification_template_model import NotificationTemplate
from models.notification_model import NotificationGroup, NotificationChannel

def init_data():
    db = SessionLocal()
    try:
        # 检查并初始化告警规则
        alert_rules = [
            AlertRule(
                name="CPU使用率告警",
                description="监控CPU使用率超过阈值",
                severity=2,
                condition_type="threshold",
                threshold=80,
                check_interval=300,
                notification_channels="email,dingtalk",
                is_active=True
            ),
            AlertRule(
                name="内存使用率告警",
                description="监控内存使用率超过阈值",
                severity=2,
                condition_type="threshold",
                threshold=85,
                check_interval=300,
                notification_channels="email,dingtalk",
                is_active=True
            ),
            AlertRule(
                name="磁盘空间告警",
                description="监控磁盘空间使用率超过阈值",
                severity=3,
                condition_type="threshold",
                threshold=90,
                check_interval=600,
                notification_channels="email,dingtalk,wechat",
                is_active=True
            )
        ]
        
        # 初始化通知模板
        notification_templates = [
            NotificationTemplate(
                name="默认邮件模板",
                description="系统默认邮件通知模板",
                template_type="email",
                content="""告警通知

告警名称：${alert_name}
告警级别：${severity}
告警时间：${alert_time}
告警描述：${description}

当前值：${current_value}
阈值：${threshold}

请及时处理！""",
                variables={
                    "alert_name": "告警名称",
                    "severity": "告警级别",
                    "alert_time": "告警时间",
                    "description": "告警描述",
                    "current_value": "当前值",
                    "threshold": "阈值"
                },
                language="zh-CN"
            ),
            NotificationTemplate(
                name="默认钉钉模板",
                description="系统默认钉钉通知模板",
                template_type="dingtalk",
                content="""### 告警通知
- 告警名称：${alert_name}
- 告警级别：${severity}
- 告警时间：${alert_time}
- 告警描述：${description}
- 当前值：${current_value}
- 阈值：${threshold}

请及时处理！""",
                variables={
                    "alert_name": "告警名称",
                    "severity": "告警级别",
                    "alert_time": "告警时间",
                    "description": "告警描述",
                    "current_value": "当前值",
                    "threshold": "阈值"
                },
                language="zh-CN"
            )
        ]
        
        # 初始化通知组
        notification_groups = [
            NotificationGroup(
                name="运维组",
                description="运维团队通知组",
                members=[
                    {"name": "张三", "email": "zhangsan@example.com", "phone": "13800138000"},
                    {"name": "李四", "email": "lisi@example.com", "phone": "13800138001"}
                ]
            ),
            NotificationGroup(
                name="开发组",
                description="开发团队通知组",
                members=[
                    {"name": "王五", "email": "wangwu@example.com", "phone": "13800138002"},
                    {"name": "赵六", "email": "zhaoliu@example.com", "phone": "13800138003"}
                ]
            )
        ]
        
        # 初始化通知渠道
        notification_channels = [
            NotificationChannel(
                name="默认邮件通道",
                channel_type="email",
                config={
                    "smtp_server": "smtp.example.com",
                    "smtp_port": 587,
                    "username": "alert@example.com",
                    "password": "your-password",
                    "use_tls": True
                }
            ),
            NotificationChannel(
                name="默认钉钉通道",
                channel_type="dingtalk",
                config={
                    "webhook_url": "https://oapi.dingtalk.com/robot/send?access_token=your-token",
                    "secret": "your-secret"
                }
            ),
            NotificationChannel(
                name="默认企业微信通道",
                channel_type="wechat",
                config={
                    "webhook_url": "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=your-key"
                }
            )
        ]
        
        # 检查并添加告警规则
        for rule in alert_rules:
            existing_rule = db.query(AlertRule).filter(AlertRule.name == rule.name).first()
            if not existing_rule:
                db.add(rule)
            
        # 检查并添加通知模板
        for template in notification_templates:
            existing_template = db.query(NotificationTemplate).filter(NotificationTemplate.name == template.name).first()
            if not existing_template:
                db.add(template)
                
        # 检查并添加通知组
        for group in notification_groups:
            existing_group = db.query(NotificationGroup).filter(NotificationGroup.name == group.name).first()
            if not existing_group:
                db.add(group)
                
        # 检查并添加通知渠道
        for channel in notification_channels:
            existing_channel = db.query(NotificationChannel).filter(NotificationChannel.name == channel.name).first()
            if not existing_channel:
                db.add(channel)
                
        # 批量添加新的告警规则
        if alert_rules:
            db.add_all(alert_rules)
        
        # 提交事务
        db.commit()
        print("初始化数据完成！")
        
    except Exception as e:
        print(f"初始化数据失败：{str(e)}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_data()