import { categoryConfigs } from "../app/categoryConfig";

import { Card } from "./ui/card";
import { Badge } from "./ui/badge";
import { ScrollArea } from "./ui/scroll-area";
import { ImageWithFallback } from "./figma/ImageWithFallback";
import { motion } from "framer-motion";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  LineChart,
  Line,
  Area,
  AreaChart,
} from "recharts";
import {
  Clock,
  TrendingUp,
  TrendingDown,
  Activity as ActivityIcon,
  Sparkles,
  Target,
  Zap,
  Brain,
  Calendar,
} from "lucide-react";
import { Progress } from "./ui/progress";
import { useGetActivitiesQuery } from "../services/activitiesApi";

export function Dashboard() {
  const productiveCategories = ["work", "learning", "exercise"];
  const neutralCategories = ["admin", "commute", "social"];
  const wastedCategories = ["leisure", "sleep", "other"];
  const normalizeActivity = (act) => ({
    ...act,
    summary_category: Array.isArray(act.summary_category)
      ? act.summary_category
      : act.summary_category
        ? [act.summary_category]
        : [],
  });
 

 
  const { data: rawActivities = [] } = useGetActivitiesQuery();

  const activities = rawActivities.map(normalizeActivity);

  const weekDays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];

  const weeklyData = weekDays.map((day) => {
    const dayMinutes = Math.floor(Math.random() * 400) + 200;
    const productiveMinutes = Math.floor(
      dayMinutes * (0.4 + Math.random() * 0.4),
    );
    return {
      day,
      total: dayMinutes / 60,
      productive: productiveMinutes / 60,
      nonProductive: (dayMinutes - productiveMinutes) / 60,
    };
  });

  const todayCategories = {};
  activities.slice(0, 6).forEach((act) => {
    act.summary_category.forEach((cat) => {
      todayCategories[cat] = (todayCategories[cat] || 0) + act.duration_minutes;
    });
  });

  const todayData = Object.entries(todayCategories).map(([cat, minutes]) => ({
    name: categoryConfigs[cat]?.label || cat,
    value: minutes,
    category: cat,
  }));

  const mostFocusedCategory =
    todayData.length > 0
      ? todayData.reduce((max, curr) => (curr.value > max.value ? curr : max))
      : null;

  const productivityTrend = Array.from({ length: 7 }, (_, i) => ({
    day: new Date(
      Date.now() - (6 - i) * 24 * 60 * 60 * 1000,
    ).toLocaleDateString("en-US", { weekday: "short" }),
    score: 55 + Math.random() * 30,
    baseline: 65,
  }));

  const totalMinutes = activities.reduce(
    (sum, act) => sum + act.duration_minutes,
    0,
  );

  const productiveMinutes = activities.reduce((sum, act) => {
    const hasProductive = act.summary_category.some((cat) =>
      productiveCategories.includes(cat),
    );
    return hasProductive ? sum + act.duration_minutes : sum;
  }, 0);

  const productivityPercentage =
    totalMinutes > 0 ? Math.round((productiveMinutes / totalMinutes) * 100) : 0;

  const wastedInvestedData = [
    {
      name: "Productive",
      value: productiveMinutes,
      color: "#10b981",
    },
    {
      name: "Neutral",
      value: activities.reduce((sum, act) => {
        const hasNeutral = act.summary_category.some((cat) =>
          neutralCategories.includes(cat),
        );
        return hasNeutral ? sum + act.duration_minutes : sum;
      }, 0),
      color: "#f59e0b",
    },
    {
      name: "Wasted",
      value: activities.reduce((sum, act) => {
        const hasWasted = act.summary_category.some((cat) =>
          wastedCategories.includes(cat),
        );
        return hasWasted ? sum + act.duration_minutes : sum;
      }, 0),
      color: "#ef4444",
    },
  ];

  const recentActivities = [...activities]
    .sort(
      (a, b) => new Date(b.start_ts).getTime() - new Date(a.start_ts).getTime(),
    )
    .slice(0, 8);

  const getTimeAgo = (timestamp) => {
    const now = new Date();
    const then = new Date(timestamp);
    const diffMs = now.getTime() - then.getTime();
    const diffHours = Math.floor(diffMs / (1000 * 60 * 60));
    const diffMins = Math.floor(diffMs / (1000 * 60));
    if (diffHours > 24) return `${Math.floor(diffHours / 24)}d ago`;
    if (diffHours > 0) return `${diffHours}h ago`;
    return `${diffMins}m ago`;
  };

  const insights = [
    {
      icon: Calendar,
      text: "You are most productive on Tuesdays.",
      trend: "up",
    },
    { icon: Clock, text: "Your productivity drops after 9 PM.", trend: "down" },
    { icon: Zap, text: "Coding gives you highest focus score.", trend: "up" },
    {
      icon: TrendingUp,
      text: "Entertainment time increased 18% this week.",
      trend: "neutral",
    },
  ];

  const COLORS = [
    "#8b5cf6",
    "#3b82f6",
    "#10b981",
    "#f59e0b",
    "#ef4444",
    "#ec4899",
    "#06b6d4",
    "#6366f1",
  ];
  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-950 via-gray-900 to-gray-950 text-white p-6">
      <div className="max-w-[1600px] mx-auto space-y-6">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="flex items-center justify-between mb-8"
        >
          <div>
            <h1 className="text-4xl font-bold bg-gradient-to-r from-blue-400 via-purple-400 to-pink-400 bg-clip-text text-transparent mb-2">
              Productivity Analytics
            </h1>
            <p className="text-gray-400 text-lg">
              Track your progress and achieve your goals
            </p>
          </div>
        </motion.div>

        {/* Top Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.1 }}
          >
            <Card className="bg-gradient-to-br from-blue-500/10 to-blue-600/10 backdrop-blur-xl border border-blue-500/20 p-6 hover:border-blue-400/40 transition-all">
              <div className="flex items-center justify-between mb-3">
                <div className="p-3 bg-blue-500/20 rounded-xl">
                  <ActivityIcon className="w-6 h-6 text-blue-400" />
                </div>
                <Badge className="bg-green-500/20 text-green-400 border-0">
                  +3 this week
                </Badge>
              </div>
              <p className="text-3xl font-bold text-white mb-1">
                {activities.length}
              </p>
              <p className="text-sm text-gray-400">Total Activities</p>
            </Card>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.2 }}
          >
            <Card className="bg-gradient-to-br from-purple-500/10 to-purple-600/10 backdrop-blur-xl border border-purple-500/20 p-6 hover:border-purple-400/40 transition-all">
              <div className="flex items-center justify-between mb-3">
                <div className="p-3 bg-purple-500/20 rounded-xl">
                  <Clock className="w-6 h-6 text-purple-400" />
                </div>
                <Badge className="bg-green-500/20 text-green-400 border-0">
                  +12h this week
                </Badge>
              </div>
              <p className="text-3xl font-bold text-white mb-1">
                {Math.floor(totalMinutes / 60)}h
              </p>
              <p className="text-sm text-gray-400">Total Hours</p>
            </Card>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.3 }}
          >
            <Card className="bg-gradient-to-br from-green-500/10 to-green-600/10 backdrop-blur-xl border border-green-500/20 p-6 hover:border-green-400/40 transition-all">
              <div className="flex items-center justify-between mb-3">
                <div className="p-3 bg-green-500/20 rounded-xl">
                  <Target className="w-6 h-6 text-green-400" />
                </div>
                <Badge className="bg-green-500/20 text-green-400 border-0">
                  +5% this month
                </Badge>
              </div>
              <p className="text-3xl font-bold text-white mb-1">
                {productivityPercentage}%
              </p>
              <p className="text-sm text-gray-400">Productivity Score</p>
            </Card>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.4 }}
          >
            <Card className="bg-gradient-to-br from-pink-500/10 to-pink-600/10 backdrop-blur-xl border border-pink-500/20 p-6 hover:border-pink-400/40 transition-all">
              <div className="flex items-center justify-between mb-3">
                <div className="p-3 bg-pink-500/20 rounded-xl">
                  <Zap className="w-6 h-6 text-pink-400" />
                </div>
                <Badge className="bg-yellow-500/20 text-yellow-400 border-0">
                  Peak hours
                </Badge>
              </div>
              <p className="text-3xl font-bold text-white mb-1">9-5</p>
              <p className="text-sm text-gray-400">Most Productive</p>
            </Card>
          </motion.div>
        </div>

        {/* Main Charts Row */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Weekly Time Distribution */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.5 }}
          >
            <Card className="bg-gray-900/50 backdrop-blur-xl border border-gray-800/50 p-6 h-full">
              <div className="mb-6">
                <h3 className="text-xl font-bold text-white mb-1">
                  Weekly Time Distribution
                </h3>
                <p className="text-sm text-gray-400">
                  Total time spent each day
                </p>
              </div>
              <ResponsiveContainer width="100%" height={280}>
                <BarChart data={weeklyData}>
                  <defs>
                    <linearGradient
                      id="productiveGradient"
                      x1="0"
                      y1="0"
                      x2="0"
                      y2="1"
                    >
                      <stop offset="0%" stopColor="#10b981" stopOpacity={0.8} />
                      <stop
                        offset="100%"
                        stopColor="#10b981"
                        stopOpacity={0.3}
                      />
                    </linearGradient>
                    <linearGradient
                      id="nonProductiveGradient"
                      x1="0"
                      y1="0"
                      x2="0"
                      y2="1"
                    >
                      <stop offset="0%" stopColor="#6b7280" stopOpacity={0.8} />
                      <stop
                        offset="100%"
                        stopColor="#6b7280"
                        stopOpacity={0.3}
                      />
                    </linearGradient>
                  </defs>
                  <CartesianGrid
                    strokeDasharray="3 3"
                    stroke="#374151"
                    opacity={0.3}
                  />
                  <XAxis dataKey="day" stroke="#9ca3af" />
                  <YAxis stroke="#9ca3af" />
                  <Tooltip
                    contentStyle={{
                      backgroundColor: "#1f2937",
                      border: "1px solid #374151",
                      borderRadius: "8px",
                      color: "#fff",
                    }}
                  />
                  <Legend />
                  <Bar
                    dataKey="productive"
                    fill="url(#productiveGradient)"
                    radius={[8, 8, 0, 0]}
                    name="Productive"
                  />
                  <Bar
                    dataKey="nonProductive"
                    fill="url(#nonProductiveGradient)"
                    radius={[8, 8, 0, 0]}
                    name="Non-Productive"
                  />
                </BarChart>
              </ResponsiveContainer>
            </Card>
          </motion.div>

          {/* Today's Activity */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.6 }}
          >
            <Card className="bg-gray-900/50 backdrop-blur-xl border border-gray-800/50 p-6 h-full">
              <div className="mb-6">
                <h3 className="text-xl font-bold text-white mb-1">
                  Today's Activity
                </h3>
                <p className="text-sm text-gray-400">
                  Most Focused: {mostFocusedCategory?.name || "N/A"} (
                  {mostFocusedCategory
                    ? Math.round(
                        (mostFocusedCategory.value /
                          todayData.reduce((sum, d) => sum + d.value, 0)) *
                          100,
                      )
                    : 0}
                  %)
                </p>
              </div>
              <ResponsiveContainer width="100%" height={280}>
                <PieChart>
                  <Pie
                    data={todayData}
                    cx="50%"
                    cy="50%"
                    innerRadius={60}
                    outerRadius={100}
                    paddingAngle={5}
                    dataKey="value"
                    label={({ name, percent }) =>
                      `${name} ${(percent * 100).toFixed(0)}%`
                    }
                  >
                    {todayData.map((entry, index) => (
                      <Cell
                        key={`cell-${index}`}
                        fill={COLORS[index % COLORS.length]}
                      />
                    ))}
                  </Pie>
                  <Tooltip
                    contentStyle={{
                      backgroundColor: "#1f2937",
                      border: "1px solid #374151",
                      borderRadius: "8px",
                      color: "#fff",
                    }}
                  />
                </PieChart>
              </ResponsiveContainer>
            </Card>
          </motion.div>
        </div>

        {/* Productivity Trend & Score */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Productivity Trend */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.7 }}
            className="lg:col-span-2"
          >
            <Card className="bg-gray-900/50 backdrop-blur-xl border border-gray-800/50 p-6 h-full">
              <div className="mb-6">
                <h3 className="text-xl font-bold text-white mb-1">
                  Productivity Trend
                </h3>
                <p className="text-sm text-gray-400">Last 7 days performance</p>
              </div>
              <ResponsiveContainer width="100%" height={250}>
                <LineChart data={productivityTrend}>
                  <defs>
                    <linearGradient
                      id="scoreGradient"
                      x1="0"
                      y1="0"
                      x2="0"
                      y2="1"
                    >
                      <stop offset="0%" stopColor="#8b5cf6" stopOpacity={0.8} />
                      <stop
                        offset="100%"
                        stopColor="#8b5cf6"
                        stopOpacity={0.1}
                      />
                    </linearGradient>
                  </defs>
                  <CartesianGrid
                    strokeDasharray="3 3"
                    stroke="#374151"
                    opacity={0.3}
                  />
                  <XAxis dataKey="day" stroke="#9ca3af" />
                  <YAxis stroke="#9ca3af" domain={[0, 100]} />
                  <Tooltip
                    contentStyle={{
                      backgroundColor: "#1f2937",
                      border: "1px solid #374151",
                      borderRadius: "8px",
                      color: "#fff",
                    }}
                  />
                  <Legend />
                  <Line
                    type="monotone"
                    dataKey="score"
                    stroke="#8b5cf6"
                    strokeWidth={3}
                    dot={{ fill: "#8b5cf6", r: 5 }}
                    activeDot={{ r: 7 }}
                    name="Productivity Score"
                  />
                  <Line
                    type="monotone"
                    dataKey="baseline"
                    stroke="#6b7280"
                    strokeWidth={2}
                    strokeDasharray="5 5"
                    dot={false}
                    name="Average Baseline"
                  />
                </LineChart>
              </ResponsiveContainer>
            </Card>
          </motion.div>

          {/* Productivity Score Ring */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.8 }}
          >
            <Card className="bg-gray-900/50 backdrop-blur-xl border border-gray-800/50 p-6 h-full flex flex-col items-center justify-center">
              <h3 className="text-lg font-bold text-white mb-6">
                Productivity Score
              </h3>
              <div className="relative w-40 h-40 mb-6">
                <svg className="w-full h-full transform -rotate-90">
                  <circle
                    cx="80"
                    cy="80"
                    r="70"
                    stroke="#374151"
                    strokeWidth="12"
                    fill="none"
                  />
                  <circle
                    cx="80"
                    cy="80"
                    r="70"
                    stroke="url(#ringGradient)"
                    strokeWidth="12"
                    fill="none"
                    strokeDasharray={`${(productivityPercentage / 100) * 440} 440`}
                    strokeLinecap="round"
                  />
                  <defs>
                    <linearGradient
                      id="ringGradient"
                      x1="0%"
                      y1="0%"
                      x2="100%"
                      y2="100%"
                    >
                      <stop offset="0%" stopColor="#10b981" />
                      <stop offset="100%" stopColor="#3b82f6" />
                    </linearGradient>
                  </defs>
                </svg>
                <div className="absolute inset-0 flex items-center justify-center">
                  <span className="text-4xl font-bold text-white">
                    {productivityPercentage}%
                  </span>
                </div>
              </div>
              <div className="space-y-2 w-full">
                <div className="flex justify-between text-sm">
                  <span className="text-gray-400">Weekly Avg</span>
                  <span className="text-white font-semibold">
                    {productivityPercentage - 3}%
                  </span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-gray-400">Monthly Avg</span>
                  <span className="text-white font-semibold">
                    {productivityPercentage - 5}%
                  </span>
                </div>
              </div>
            </Card>
          </motion.div>
        </div>

        {/* Bottom Row: Time Wasted/Invested + Recent Activities + Insights */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Time Wasted vs Invested */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.9 }}
          >
            <Card className="bg-gray-900/50 backdrop-blur-xl border border-gray-800/50 p-6 h-full">
              <div className="mb-6">
                <h3 className="text-xl font-bold text-white mb-1">
                  Time Analysis
                </h3>
                <p className="text-sm text-gray-400">How you spend your time</p>
              </div>
              <ResponsiveContainer width="100%" height={220}>
                <PieChart>
                  <Pie
                    data={wastedInvestedData}
                    cx="50%"
                    cy="50%"
                    innerRadius={50}
                    outerRadius={80}
                    paddingAngle={3}
                    dataKey="value"
                  >
                    {wastedInvestedData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </Pie>
                  <Tooltip
                    contentStyle={{
                      backgroundColor: "#1f2937",
                      border: "1px solid #374151",
                      borderRadius: "8px",
                      color: "#fff",
                    }}
                  />
                </PieChart>
              </ResponsiveContainer>
              <div className="space-y-2 mt-4">
                {wastedInvestedData.map((item) => (
                  <div
                    key={item.name}
                    className="flex items-center justify-between"
                  >
                    <div className="flex items-center gap-2">
                      <div
                        className="w-3 h-3 rounded-full"
                        style={{ backgroundColor: item.color }}
                      />
                      <span className="text-sm text-gray-400">{item.name}</span>
                    </div>
                    <span className="text-sm text-white font-semibold">
                      {Math.round(item.value / 60)}h
                    </span>
                  </div>
                ))}
              </div>
            </Card>
          </motion.div>

          {/* Recent Activities */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 1.0 }}
          >
            <Card className="bg-gray-900/50 backdrop-blur-xl border border-gray-800/50 p-6 h-full">
              <div className="mb-4">
                <h3 className="text-xl font-bold text-white mb-1">
                  Recent Activities
                </h3>
                <p className="text-sm text-gray-400">Latest first</p>
              </div>
              <ScrollArea className="h-[280px]">
                <div className="space-y-3">
                  {recentActivities.map((activity) => {
                    const primaryCat = activity.summary_category[0];
                    const config = categoryConfigs[primaryCat];
                    return (
                      <div
                        key={activity.id}
                        className="flex items-center gap-3 p-2 rounded-lg hover:bg-gray-800/50 transition-colors cursor-pointer"
                      >
                        <div className="w-12 h-12 rounded-lg overflow-hidden flex-shrink-0">
                          <ImageWithFallback
                            src={config.image}
                            alt={config.label}
                            className="w-full h-full object-cover"
                          />
                        </div>
                        <div className="flex-1 min-w-0">
                          <p className="text-sm font-medium text-white truncate">
                            {activity.activity_name}
                          </p>
                          <div className="flex items-center gap-2 text-xs text-gray-400">
                            <span>{activity.duration_minutes}m</span>
                            <span>•</span>
                            <span>{getTimeAgo(activity.start_ts)}</span>
                          </div>
                        </div>
                      </div>
                    );
                  })}
                </div>
              </ScrollArea>
            </Card>
          </motion.div>

          {/* Smart Insights */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 1.1 }}
          >
            <Card className="bg-gray-900/50 backdrop-blur-xl border border-gray-800/50 p-6 h-full">
              <div className="mb-4 flex items-center gap-2">
                <div className="p-2 bg-purple-500/20 rounded-lg">
                  <Brain className="w-5 h-5 text-purple-400" />
                </div>
                <div>
                  <h3 className="text-xl font-bold text-white">
                    Smart Insights
                  </h3>
                  <p className="text-xs text-gray-400">AI-powered analysis</p>
                </div>
              </div>
              <div className="space-y-3">
                {insights.map((insight, index) => {
                  const Icon = insight.icon;
                  return (
                    <motion.div
                      key={index}
                      initial={{ opacity: 0, x: -20 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ delay: 1.2 + index * 0.1 }}
                      className="bg-gray-800/30 backdrop-blur-sm p-4 rounded-xl border border-gray-700/50 hover:border-gray-600/50 transition-all"
                    >
                      <div className="flex items-start gap-3">
                        <div
                          className={`p-2 rounded-lg flex-shrink-0 ${
                            insight.trend === "up"
                              ? "bg-green-500/20"
                              : insight.trend === "down"
                                ? "bg-red-500/20"
                                : "bg-blue-500/20"
                          }`}
                        >
                          <Icon
                            className={`w-4 h-4 ${
                              insight.trend === "up"
                                ? "text-green-400"
                                : insight.trend === "down"
                                  ? "text-red-400"
                                  : "text-blue-400"
                            }`}
                          />
                        </div>
                        <p className="text-sm text-gray-300 leading-relaxed">
                          {insight.text}
                        </p>
                      </div>
                    </motion.div>
                  );
                })}
              </div>
            </Card>
          </motion.div>
        </div>
      </div>
    </div>
  );
}
