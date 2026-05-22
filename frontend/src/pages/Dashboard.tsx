import React, { useEffect, useState } from 'react';
import api from '../api/axios';
import type { CronTask, ApiMetricSummary } from '../types';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { Activity, CheckCircle, XCircle, Clock, LogOut } from 'lucide-react';
import { useAuthStore } from '../store/authStore';
import { useNavigate } from 'react-router-dom';

const Dashboard: React.FC = () => {
  const [tasks, setTasks] = useState<CronTask[]>([]);
  const [summary, setSummary] = useState<ApiMetricSummary[]>([]);
  const logout = useAuthStore((state) => state.logout);
  const navigate = useNavigate();

  const fetchData = async () => {
    try {
      const [tasksRes, summaryRes] = await Promise.all([
        api.get('/api/cron-tasks'),
        api.get('/api/dashboard/summary')
      ]);
      setTasks(tasksRes.data);
      setSummary(summaryRes.data);
    } catch (err) {
      console.error('Failed to fetch data', err);
    }
  };

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 30000);
    return () => clearInterval(interval);
  }, []);

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const successTasks = tasks.filter(t => t.status === 'success').length;
  const failedTasks = tasks.filter(t => t.status === 'failed').length;

  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16 items-center">
            <h1 className="text-xl font-bold text-purple-600">K-Metric Dashboard</h1>
            <button
              onClick={handleLogout}
              className="flex items-center text-gray-600 hover:text-purple-600 transition-colors"
            >
              <LogOut className="h-5 w-5 mr-1" />
              Logout
            </button>
          </div>
        </div>
      </nav>

      <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        {/* Stats */}
        <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4 mb-8">
          <StatCard title="Total Tasks" value={tasks.length} icon={<Activity className="text-blue-500" />} />
          <StatCard title="Successful" value={successTasks} icon={<CheckCircle className="text-green-500" />} />
          <StatCard title="Failed" value={failedTasks} icon={<XCircle className="text-red-500" />} />
          <StatCard title="Avg. API Time" value={`${summary.length > 0 ? (summary.reduce((acc, s) => acc + s.avg_response_time, 0) / summary.length).toFixed(0) : 0}ms`} icon={<Clock className="text-purple-500" />} />
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Chart */}
          <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-100">
            <h3 className="text-lg font-medium text-gray-900 mb-4">API Response Times (Avg)</h3>
            <div className="h-64">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={summary}>
                  <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f0f0f0" />
                  <XAxis dataKey="hour" tickFormatter={(t) => new Date(t).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })} />
                  <YAxis />
                  <Tooltip labelFormatter={(t) => new Date(t).toLocaleString()} />
                  <Line type="monotone" dataKey="avg_response_time" stroke="#8b5cf6" strokeWidth={2} dot={{ fill: '#8b5cf6' }} />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </div>

          {/* Cron Tasks Table */}
          <div className="bg-white rounded-lg shadow-sm border border-gray-100 overflow-hidden">
            <div className="px-6 py-4 border-b border-gray-100">
              <h3 className="text-lg font-medium text-gray-900">Recent Cron Tasks</h3>
            </div>
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-200">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Task</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Runtime</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Executed At</th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {tasks.slice(0, 10).map((task) => (
                    <tr key={task.id}>
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{task.name}</td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${task.status === 'success' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}`}>
                          {task.status}
                        </span>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{task.runtime}s</td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{new Date(task.executed_at).toLocaleString()}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
};

const StatCard: React.FC<{ title: string; value: string | number; icon: React.ReactNode }> = ({ title, value, icon }) => (
  <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-100 flex items-center">
    <div className="p-3 rounded-full bg-gray-50 mr-4">
      {icon}
    </div>
    <div>
      <p className="text-sm font-medium text-gray-500 uppercase">{title}</p>
      <p className="text-2xl font-bold text-gray-900">{value}</p>
    </div>
  </div>
);

export default Dashboard;
