import { useState } from "react";
import {
  Target,
  CheckSquare,
  ListTodo,
  Bot,
  TrendingUp,
  Calendar,
  Award,
} from "lucide-react";
import { useNavigate } from "react-router-dom";
import { Button } from "./ui/button";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "./ui/tabs";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "./ui/card";
import { Progress } from "./ui/progress";
import {
  AreaChart,
  Area,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
} from "recharts";

export function Dashboard(
 
) {
  const [activeTab, setActiveTab] = useState("overview");
  
  const navigate = useNavigate();

  // Mock data for charts
  const weeklyProgress = [
    { day: "Mon", completed: 12, total: 15 },
    { day: "Tue", completed: 18, total: 20 },
    { day: "Wed", completed: 15, total: 18 },
    { day: "Thu", completed: 22, total: 25 },
    { day: "Fri", completed: 20, total: 22 },
    { day: "Sat", completed: 10, total: 12 },
    { day: "Sun", completed: 8, total: 10 },
  ];

  const categoryData = [
    { name: "Goals", value: 12, color: "#8B5CF6" },
    { name: "Tasks", value: 45, color: "#3B82F6" },
    { name: "Subtasks", value: 78, color: "#EC4899" },
  ];

  const recentActivity = [
    {
      id: 1,
      type: "goal",
      title: "Launch Personal Website",
      status: "In Progress",
      progress: 65,
    },
    {
      id: 2,
      type: "task",
      title: "Morning Workout Routine",
      status: "Completed",
      progress: 100,
    },
    {
      id: 3,
      type: "subtask",
      title: "Review Design Mockups",
      status: "Pending",
      progress: 30,
    },
    {
      id: 4,
      type: "goal",
      title: "Learn React Advanced Patterns",
      status: "In Progress",
      progress: 45,
    },
  ];

  const stats = [
    {
      label: "Total Goals",
      value: "12",
      change: "+3 this week",
      icon: Target,
      color: "bg-purple-500",
    },
    {
      label: "Active Tasks",
      value: "45",
      change: "+12 this week",
      icon: CheckSquare,
      color: "bg-blue-500",
    },
    {
      label: "Subtasks",
      value: "78",
      change: "+25 this week",
      icon: ListTodo,
      color: "bg-pink-500",
    },
    {
      label: "Completion Rate",
      value: "87%",
      change: "+5% this month",
      icon: TrendingUp,
      color: "bg-green-500",
    },
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-purple-50 to-indigo-100">
      <div className="max-w-7xl mx-auto px-6 py-8">
        {/* Header */}
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-4xl font-bold text-gray-900 mb-2">
              Life OS Dashboard
            </h1>
            <p className="text-gray-600">
              Track your progress and achieve your goals
            </p>
          </div>

          {/* AI Chatbot Button */}
          <Button onClick={() => navigate("/planner")} className="relative bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-700 hover:to-indigo-700 text-white px-6 h-12 group">
            <Bot className="w-5 h-5 mr-2 animate-pulse" />
            AI Planner
            <span className="absolute -top-1 -right-1 flex h-3 w-3">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75"></span>
              <span className="relative inline-flex rounded-full h-3 w-3 bg-green-500"></span>
            </span>
          </Button>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          {stats.map((stat, index) => (
            <Card key={index} className="hover:shadow-lg transition-shadow">
              <CardContent className="p-6">
                <div className="flex items-center justify-between mb-4">
                  <div className={`${stat.color} p-3 rounded-xl`}>
                    <stat.icon className="w-6 h-6 text-white" />
                  </div>
                  <span className="text-sm text-green-600 font-medium">
                    {stat.change}
                  </span>
                </div>
                <h3 className="text-2xl font-bold text-gray-900 mb-1">
                  {stat.value}
                </h3>
                <p className="text-sm text-gray-600">{stat.label}</p>
              </CardContent>
            </Card>
          ))}
        </div>

        {/* Main Content with Tabs */}
        <Tabs
          value={activeTab}
          onValueChange={setActiveTab}
          className="space-y-6"
        >
          <TabsList className="bg-white p-1 rounded-xl shadow-md">
            <TabsTrigger
              value="overview"
              className="px-6 data-[state=active]:bg-gradient-to-r data-[state=active]:from-purple-600 data-[state=active]:to-indigo-600 data-[state=active]:text-white"
            >
              Overview
            </TabsTrigger>
            <TabsTrigger
              value="goals"
              className="px-6 data-[state=active]:bg-gradient-to-r data-[state=active]:from-purple-600 data-[state=active]:to-indigo-600 data-[state=active]:text-white"
            >
              Goals
            </TabsTrigger>
            <TabsTrigger
              value="tasks"
              className="px-6 data-[state=active]:bg-gradient-to-r data-[state=active]:from-purple-600 data-[state=active]:to-indigo-600 data-[state=active]:text-white"
            >
              Tasks
            </TabsTrigger>
            <TabsTrigger
              value="subtasks"
              className="px-6 data-[state=active]:bg-gradient-to-r data-[state=active]:from-purple-600 data-[state=active]:to-indigo-600 data-[state=active]:text-white"
            >
              Subtasks
            </TabsTrigger>
          </TabsList>

          {/* Overview Tab */}
          <TabsContent value="overview" className="space-y-6">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {/* Weekly Progress Chart */}
              <Card>
                <CardHeader>
                  <CardTitle>Weekly Progress</CardTitle>
                  <CardDescription>
                    Your completion rate this week
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <ResponsiveContainer width="100%" height={300}>
                    <AreaChart data={weeklyProgress}>
                      <defs>
                        <linearGradient
                          id="colorCompleted"
                          x1="0"
                          y1="0"
                          x2="0"
                          y2="1"
                        >
                          <stop
                            offset="5%"
                            stopColor="#8B5CF6"
                            stopOpacity={0.8}
                          />
                          <stop
                            offset="95%"
                            stopColor="#8B5CF6"
                            stopOpacity={0}
                          />
                        </linearGradient>
                      </defs>
                      <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                      <XAxis dataKey="day" stroke="#6b7280" />
                      <YAxis stroke="#6b7280" />
                      <Tooltip />
                      <Area
                        type="monotone"
                        dataKey="completed"
                        stroke="#8B5CF6"
                        fillOpacity={1}
                        fill="url(#colorCompleted)"
                      />
                    </AreaChart>
                  </ResponsiveContainer>
                </CardContent>
              </Card>

              {/* Category Distribution */}
              <Card>
                <CardHeader>
                  <CardTitle>Category Distribution</CardTitle>
                  <CardDescription>
                    Breakdown of your activities
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <ResponsiveContainer width="100%" height={300}>
                    <PieChart>
                      <Pie
                        data={categoryData}
                        cx="50%"
                        cy="50%"
                        labelLine={false}
                        label={({ name, percent }) =>
                          `${name} ${(percent * 100).toFixed(0)}%`
                        }
                        outerRadius={100}
                        fill="#8884d8"
                        dataKey="value"
                      >
                        {categoryData.map((entry, index) => (
                          <Cell key={`cell-${index}`} fill={entry.color} />
                        ))}
                      </Pie>
                      <Tooltip />
                    </PieChart>
                  </ResponsiveContainer>
                </CardContent>
              </Card>
            </div>

            {/* Recent Activity */}
            <Card>
              <CardHeader>
                <CardTitle>Recent Activity</CardTitle>
                <CardDescription>
                  Your latest updates across all categories
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {recentActivity.map((activity) => (
                    <div
                      key={activity.id}
                      className="flex items-center justify-between p-4 bg-gradient-to-r from-purple-50 to-indigo-50 rounded-xl hover:shadow-md transition-shadow"
                    >
                      <div className="flex-1">
                        <div className="flex items-center gap-3 mb-2">
                          <span
                            className={`px-3 py-1 rounded-full text-xs font-medium ${
                              activity.type === "goal"
                                ? "bg-purple-200 text-purple-700"
                                : activity.type === "task"
                                ? "bg-blue-200 text-blue-700"
                                : "bg-pink-200 text-pink-700"
                            }`}
                          >
                            {activity.type}
                          </span>
                          <h4 className="font-semibold text-gray-900">
                            {activity.title}
                          </h4>
                        </div>
                        <div className="flex items-center gap-4">
                          <Progress
                            value={activity.progress}
                            className="flex-1"
                          />
                          <span className="text-sm text-gray-600 font-medium">
                            {activity.progress}%
                          </span>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Goals Tab */}
          <TabsContent value="goals">
            <Card>
              <CardHeader>
                <div className="flex items-center justify-between">
                  <div>
                    <CardTitle>Your Goals</CardTitle>
                    <CardDescription>
                      Long-term objectives to achieve
                    </CardDescription>
                  </div>
                  <Button
                    onClick={() => navigate("/goals")}
                    className="bg-purple-600 hover:bg-purple-700"
                  >
                    View All Goals
                  </Button>
                </div>
              </CardHeader>
              <CardContent>
                <div className="text-center py-12">
                  <Target className="w-16 h-16 mx-auto text-purple-400 mb-4" />
                  <p className="text-gray-600 mb-4">
                    Click "View All Goals" to see your complete goals list
                  </p>
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Tasks Tab */}
          <TabsContent value="tasks">
            <Card>
              <CardHeader>
                <div className="flex items-center justify-between">
                  <div>
                    <CardTitle>Your Tasks</CardTitle>
                    <CardDescription>
                      Daily and weekly tasks to complete
                    </CardDescription>
                  </div>
                  <Button
                    onClick={() => navigate("/tasks")}
                    className="bg-blue-600 hover:bg-blue-700"
                  >
                    View All Tasks
                  </Button>
                </div>
              </CardHeader>
              <CardContent>
                <div className="text-center py-12">
                  <CheckSquare className="w-16 h-16 mx-auto text-blue-400 mb-4" />
                  <p className="text-gray-600 mb-4">
                    Click "View All Tasks" to see your complete tasks list
                  </p>
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Subtasks Tab */}
          <TabsContent value="subtasks">
            <Card>
              <CardHeader>
                <div className="flex items-center justify-between">
                  <div>
                    <CardTitle>Your Subtasks</CardTitle>
                    <CardDescription>
                      Smaller steps to complete your tasks
                    </CardDescription>
                  </div>
                  <Button
                    onClick={() => navigate("/subtasks")}
                    className="bg-pink-600 hover:bg-pink-700"
                  >
                    View All Subtasks
                  </Button>
                </div>
              </CardHeader>
              <CardContent>
                <div className="text-center py-12">
                  <ListTodo className="w-16 h-16 mx-auto text-pink-400 mb-4" />
                  <p className="text-gray-600 mb-4">
                    Click "View All Subtasks" to see your complete subtasks list
                  </p>
                </div>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  );
}
