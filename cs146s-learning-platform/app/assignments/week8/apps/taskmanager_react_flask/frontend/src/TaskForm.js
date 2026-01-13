import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { taskAPI } from './api';
import './TaskForm.css';

function TaskForm() {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    status: 'pending',
    priority: 'medium',
    due_date: ''
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!formData.title.trim()) {
      setError('任务标题不能为空');
      return;
    }

    try {
      setLoading(true);
      setError(null);

      // 处理日期格式
      const submitData = {
        ...formData,
        due_date: formData.due_date || null
      };

      await taskAPI.createTask(submitData);
      navigate('/tasks');
    } catch (err) {
      setError('创建任务失败，请重试');
      console.error('创建任务失败:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleCancel = () => {
    navigate('/tasks');
  };

  return (
    <div className="task-form-container">
      <div className="task-form-header">
        <h2>新建任务</h2>
      </div>

      <form onSubmit={handleSubmit} className="task-form">
        {error && <div className="error-message">{error}</div>}

        <div className="form-group">
          <label htmlFor="title">任务标题 *</label>
          <input
            type="text"
            id="title"
            name="title"
            value={formData.title}
            onChange={handleChange}
            placeholder="请输入任务标题"
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="description">任务描述</label>
          <textarea
            id="description"
            name="description"
            value={formData.description}
            onChange={handleChange}
            placeholder="请输入任务详细描述"
            rows="4"
          />
        </div>

        <div className="form-row">
          <div className="form-group">
            <label htmlFor="status">任务状态</label>
            <select
              id="status"
              name="status"
              value={formData.status}
              onChange={handleChange}
            >
              <option value="pending">待处理</option>
              <option value="in_progress">进行中</option>
              <option value="completed">已完成</option>
              <option value="cancelled">已取消</option>
            </select>
          </div>

          <div className="form-group">
            <label htmlFor="priority">优先级</label>
            <select
              id="priority"
              name="priority"
              value={formData.priority}
              onChange={handleChange}
            >
              <option value="low">低</option>
              <option value="medium">中</option>
              <option value="high">高</option>
              <option value="urgent">紧急</option>
            </select>
          </div>
        </div>

        <div className="form-group">
          <label htmlFor="due_date">截止日期</label>
          <input
            type="date"
            id="due_date"
            name="due_date"
            value={formData.due_date}
            onChange={handleChange}
          />
        </div>

        <div className="form-actions">
          <button
            type="button"
            onClick={handleCancel}
            className="btn btn-secondary"
            disabled={loading}
          >
            取消
          </button>
          <button
            type="submit"
            className="btn btn-primary"
            disabled={loading}
          >
            {loading ? '创建中...' : '创建任务'}
          </button>
        </div>
      </form>
    </div>
  );
}

export default TaskForm;
