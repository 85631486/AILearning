import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { userAPI } from './api';
import './UserList.css';

function UserList() {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedUser, setSelectedUser] = useState(null);
  const [userTasks, setUserTasks] = useState([]);

  useEffect(() => {
    fetchUsers();
  }, []);

  const fetchUsers = async () => {
    try {
      setLoading(true);
      const response = await userAPI.getAllUsers();
      setUsers(response.data);
      setError(null);
    } catch (err) {
      setError('获取用户列表失败');
      console.error('获取用户列表失败:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleViewUserTasks = async (user) => {
    try {
      const response = await userAPI.getUserTasks(user.id);
      setSelectedUser(user);
      setUserTasks(response.data);
    } catch (err) {
      alert('获取用户任务失败');
      console.error('获取用户任务失败:', err);
    }
  };

  const closeUserTasks = () => {
    setSelectedUser(null);
    setUserTasks([]);
  };

  if (loading) {
    return <div className="loading">加载中...</div>;
  }

  if (error) {
    return <div className="error">{error}</div>;
  }

  return (
    <div className="user-list-container">
      <div className="user-list-header">
        <h2>用户管理</h2>
        <div className="user-actions">
          <Link to="/users/new" className="btn btn-primary">新建用户</Link>
        </div>
      </div>

      {users.length === 0 ? (
        <div className="no-users">
          <p>暂无用户</p>
          <Link to="/users/new" className="btn btn-primary">创建第一个用户</Link>
        </div>
      ) : (
        <div className="user-grid">
          {users.map(user => (
            <div key={user.id} className="user-card">
              <div className="user-header">
                <h3>{user.name}</h3>
                <span className="user-email">{user.email}</span>
              </div>

              <div className="user-meta">
                <small>
                  创建时间: {new Date(user.created_at).toLocaleString()}
                </small>
              </div>

              <div className="user-actions">
                <button
                  onClick={() => handleViewUserTasks(user)}
                  className="btn btn-secondary btn-small"
                >
                  查看任务
                </button>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* 用户任务模态框 */}
      {selectedUser && (
        <div className="modal-overlay" onClick={closeUserTasks}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h3>{selectedUser.name} 的任务</h3>
              <button onClick={closeUserTasks} className="close-btn">&times;</button>
            </div>

            <div className="modal-body">
              {userTasks.length === 0 ? (
                <p>该用户暂无任务</p>
              ) : (
                <div className="user-tasks-list">
                  {userTasks.map(task => (
                    <div key={task.id} className="user-task-item">
                      <div className="task-info">
                        <h4>{task.title}</h4>
                        <p>{task.description}</p>
                        <div className="task-meta">
                          <span className={`status-badge status-${task.status}`}>
                            {task.status}
                          </span>
                          <span className={`priority-badge priority-${task.priority}`}>
                            {task.priority}
                          </span>
                          {task.due_date && (
                            <span className="due-date">
                              截止: {new Date(task.due_date).toLocaleDateString()}
                            </span>
                          )}
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default UserList;
