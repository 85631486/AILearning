"""
Week 4: 自主编码代理 - 基础代理框架
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
from datetime import datetime
import json


class AgentMessage:
    """代理间通信的消息"""

    def __init__(self, sender: str, receiver: str, message_type: str, content: Any, metadata: Dict = None):
        self.sender = sender
        self.receiver = receiver
        self.message_type = message_type
        self.content = content
        self.metadata = metadata or {}
        self.timestamp = datetime.now()

    def to_dict(self):
        return {
            'sender': self.sender,
            'receiver': self.receiver,
            'message_type': self.message_type,
            'content': self.content,
            'metadata': self.metadata,
            'timestamp': self.timestamp.isoformat()
        }


class BaseAgent(ABC):
    """自主编码代理基类"""

    def __init__(self, name: str, role: str, capabilities: List[str]):
        self.name = name
        self.role = role
        self.capabilities = capabilities
        self.memory: List[AgentMessage] = []
        self.tools: Dict[str, Any] = {}

    @abstractmethod
    def process_message(self, message: AgentMessage) -> AgentMessage:
        """处理接收到的消息"""
        pass

    @abstractmethod
    def generate_response(self, task: str, context: Dict) -> str:
        """生成任务响应"""
        pass

    def add_tool(self, tool_name: str, tool_func: Any):
        """添加工具到代理"""
        self.tools[tool_name] = tool_func

    def use_tool(self, tool_name: str, **kwargs) -> Any:
        """使用工具"""
        if tool_name not in self.tools:
            raise ValueError(f"工具 {tool_name} 不可用")

        return self.tools[tool_name](**kwargs)

    def remember(self, message: AgentMessage):
        """记录消息到记忆"""
        self.memory.append(message)

    def recall(self, limit: int = 10) -> List[AgentMessage]:
        """回忆最近的消息"""
        return self.memory[-limit:]

    def get_status(self) -> Dict[str, Any]:
        """获取代理状态"""
        return {
            'name': self.name,
            'role': self.role,
            'capabilities': self.capabilities,
            'tools_count': len(self.tools),
            'memory_size': len(self.memory),
            'last_activity': self.memory[-1].timestamp.isoformat() if self.memory else None
        }


class Task:
    """编码任务"""

    def __init__(self, task_id: str, description: str, requirements: List[str], priority: str = "medium"):
        self.task_id = task_id
        self.description = description
        self.requirements = requirements
        self.priority = priority
        self.status = "pending"
        self.assigned_agent = None
        self.created_at = datetime.now()
        self.completed_at = None
        self.result = None

    def assign_to(self, agent_name: str):
        """分配给代理"""
        self.assigned_agent = agent_name
        self.status = "assigned"

    def complete(self, result: Any = None):
        """标记完成"""
        self.status = "completed"
        self.completed_at = datetime.now()
        self.result = result

    def fail(self, error: str):
        """标记失败"""
        self.status = "failed"
        self.result = error

    def to_dict(self):
        return {
            'task_id': self.task_id,
            'description': self.description,
            'requirements': self.requirements,
            'priority': self.priority,
            'status': self.status,
            'assigned_agent': self.assigned_agent,
            'created_at': self.created_at.isoformat(),
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'result': self.result
        }


class AgentOrchestrator:
    """代理编排器"""

    def __init__(self):
        self.agents: Dict[str, BaseAgent] = {}
        self.tasks: Dict[str, Task] = {}
        self.message_queue: List[AgentMessage] = []

    def register_agent(self, agent: BaseAgent):
        """注册代理"""
        self.agents[agent.name] = agent

    def create_task(self, task_id: str, description: str, requirements: List[str], priority: str = "medium") -> Task:
        """创建任务"""
        task = Task(task_id, description, requirements, priority)
        self.tasks[task_id] = task
        return task

    def assign_task(self, task_id: str, agent_name: str):
        """分配任务给代理"""
        if task_id not in self.tasks:
            raise ValueError(f"任务 {task_id} 不存在")

        if agent_name not in self.agents:
            raise ValueError(f"代理 {agent_name} 不存在")

        task = self.tasks[task_id]
        task.assign_to(agent_name)

        # 发送任务分配消息
        message = AgentMessage(
            sender="orchestrator",
            receiver=agent_name,
            message_type="task_assignment",
            content={"task": task.to_dict()},
            metadata={"task_id": task_id}
        )

        self.send_message(message)

    def send_message(self, message: AgentMessage):
        """发送消息"""
        self.message_queue.append(message)

        # 如果接收者是代理，立即处理
        if message.receiver in self.agents:
            agent = self.agents[message.receiver]
            response = agent.process_message(message)

            if response:
                self.message_queue.append(response)

    def process_message_queue(self):
        """处理消息队列"""
        while self.message_queue:
            message = self.message_queue.pop(0)

            if message.receiver in self.agents:
                agent = self.agents[message.receiver]
                response = agent.process_message(message)

                if response:
                    self.message_queue.append(response)

    def get_system_status(self) -> Dict[str, Any]:
        """获取系统状态"""
        return {
            'agents': {name: agent.get_status() for name, agent in self.agents.items()},
            'tasks': {task_id: task.to_dict() for task_id, task in self.tasks.items()},
            'message_queue_size': len(self.message_queue),
            'total_tasks': len(self.tasks),
            'completed_tasks': len([t for t in self.tasks.values() if t.status == "completed"])
        }
