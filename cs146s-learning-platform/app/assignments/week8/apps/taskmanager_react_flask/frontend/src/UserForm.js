import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { userAPI } from './api';
import './UserForm.css';

function UserForm() {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    name: '',
    email: ''
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

  const validateForm = () => {
    if (!formData.name.trim()) {
      setError('用户姓名不能为空');
      return false;
    }

    if (!formData.email.trim()) {
      setError('邮箱地址不能为空');
      return false;
    }

    // 简单的邮箱格式验证
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(formData.email)) {
      setError('请输入有效的邮箱地址');
      return false;
    }

    return true;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!validateForm()) {
      return;
    }

    try {
      setLoading(true);
      setError(null);

      await userAPI.createUser(formData);
      navigate('/users');
    } catch (err) {
      if (err.response && err.response.status === 409) {
        setError('该邮箱地址已被注册');
      } else {
        setError('创建用户失败，请重试');
      }
      console.error('创建用户失败:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleCancel = () => {
    navigate('/users');
  };

  return (
    <div className="user-form-container">
      <div className="user-form-header">
        <h2>新建用户</h2>
      </div>

      <form onSubmit={handleSubmit} className="user-form">
        {error && <div className="error-message">{error}</div>}

        <div className="form-group">
          <label htmlFor="name">用户姓名 *</label>
          <input
            type="text"
            id="name"
            name="name"
            value={formData.name}
            onChange={handleChange}
            placeholder="请输入用户姓名"
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="email">邮箱地址 *</label>
          <input
            type="email"
            id="email"
            name="email"
            value={formData.email}
            onChange={handleChange}
            placeholder="请输入邮箱地址"
            required
          />
          <small className="form-help">邮箱地址将用于用户登录和通知</small>
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
            {loading ? '创建中...' : '创建用户'}
          </button>
        </div>
      </form>
    </div>
  );
}

export default UserForm;
