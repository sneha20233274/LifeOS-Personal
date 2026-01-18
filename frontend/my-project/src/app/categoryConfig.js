import {
  Briefcase,
  BookOpen,
  Dumbbell,
  Settings,
  Gamepad2,
  Moon,
  Users,
  Car,
  MoreHorizontal,
} from "lucide-react";

/**
 * JSX / JavaScript SAFE category config
 * No TS, no interfaces, no types
 */
export const categoryConfigs = {
  work: {
    name: "work",
    label: "Work",
    icon: Briefcase,
    image:
      "https://images.unsplash.com/photo-1521737604893-d14cc237f11d?w=1200&q=80",
    color: "text-blue-600",
    gradient: "from-blue-500 to-blue-600",
    bgColor: "bg-blue-50",
    borderColor: "border-blue-200",
    description: "Professional tasks and projects",
  },

  learning: {
    name: "learning",
    label: "Learning",
    icon: BookOpen,
    image:
      "https://images.unsplash.com/photo-1513258496099-48168024aec0?w=1200&q=80",
    color: "text-purple-600",
    gradient: "from-purple-500 to-purple-600",
    bgColor: "bg-purple-50",
    borderColor: "border-purple-200",
    description: "Educational activities and study",
  },

  exercise: {
    name: "exercise",
    label: "Exercise",
    icon: Dumbbell,
    image:
      "https://images.unsplash.com/photo-1554284126-aa88f22d8b74?w=1200&q=80",
    color: "text-green-600",
    gradient: "from-green-500 to-green-600",
    bgColor: "bg-green-50",
    borderColor: "border-green-200",
    description: "Physical activities and workouts",
  },

  admin: {
    name: "admin",
    label: "Admin",
    icon: Settings,
    image:
      "https://images.unsplash.com/photo-1581092160562-40aa08e78837?w=1200&q=80",
    color: "text-gray-600",
    gradient: "from-gray-500 to-gray-600",
    bgColor: "bg-gray-50",
    borderColor: "border-gray-200",
    description: "Administrative and organizational tasks",
  },

  leisure: {
    name: "leisure",
    label: "Leisure",
    icon: Gamepad2,
    image:
      "https://images.unsplash.com/photo-1605902711622-cfb43c4437b1?w=1200&q=80",
    color: "text-pink-600",
    gradient: "from-pink-500 to-pink-600",
    bgColor: "bg-pink-50",
    borderColor: "border-pink-200",
    description: "Entertainment and hobbies",
  },

  sleep: {
    name: "sleep",
    label: "Sleep",
    icon: Moon,
    image:
      "https://images.unsplash.com/photo-1541781774459-bb2af2f05b55?w=1200&q=80",
    color: "text-indigo-600",
    gradient: "from-indigo-500 to-indigo-600",
    bgColor: "bg-indigo-50",
    borderColor: "border-indigo-200",
    description: "Rest and sleep",
  },

  social: {
    name: "social",
    label: "Social",
    icon: Users,
    image:
      "https://images.unsplash.com/photo-1529156069898-49953e39b3ac?w=1200&q=80",
    color: "text-orange-600",
    gradient: "from-orange-500 to-orange-600",
    bgColor: "bg-orange-50",
    borderColor: "border-orange-200",
    description: "Social interactions and meetings",
  },

  commute: {
    name: "commute",
    label: "Commute",
    icon: Car,
    image:
      "https://images.unsplash.com/photo-1502877338535-766e1452684a?w=1200&q=80",
    color: "text-cyan-600",
    gradient: "from-cyan-500 to-cyan-600",
    bgColor: "bg-cyan-50",
    borderColor: "border-cyan-200",
    description: "Travel and transportation",
  },

  other: {
    name: "other",
    label: "Other",
    icon: MoreHorizontal,
    image:
      "https://images.unsplash.com/photo-1493612276216-ee3925520721?w=1200&q=80",
    color: "text-slate-600",
    gradient: "from-slate-500 to-slate-600",
    bgColor: "bg-slate-50",
    borderColor: "border-slate-200",
    description: "Miscellaneous activities",
  },
};
