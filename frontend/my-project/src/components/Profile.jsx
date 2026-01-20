import { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  User,
  Camera,
  Mail,
  Phone,
  MapPin,
  Calendar,
  Edit2,
  Save,
  X,
  Eye,
  EyeOff,
  Shield,
  Quote,
  Target,
  CheckCircle2,
} from "lucide-react";

import { Button } from "@/app/components/ui/button";
import { Input } from "@/app/components/ui/input";
import { Label } from "@/app/components/ui/label";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
  CardDescription,
} from "./ui/card";
import {
  Avatar,
  AvatarFallback,
  AvatarImage,
} from "./ui/avatar";
import { Badge } from "./ui/badge";
import { ImageWithFallback } from "./figma/ImageWithFallback";

const quotes = [
  {
    text: "Believe you can and you're halfway there.",
    author: "Theodore Roosevelt",
  },
  {
    text: "The only way to do great work is to love what you do.",
    author: "Steve Jobs",
  },
];

export default function ProfilePage() {
  const [quoteIndex, setQuoteIndex] = useState(0);
  const [isEditing, setIsEditing] = useState(false);
  const [showPassword, setShowPassword] = useState(false);

  const [user, setUser] = useState({
    name: "Alex Johnson",
    email: "alex@example.com",
    phone: "+1 (555) 123-4567",
    location: "San Francisco, CA",
    avatar: "",
    cover:
      "https://images.unsplash.com/photo-1548126466-4470dfd3a209?fit=crop&w=1600",
  });

  const [tempUser, setTempUser] = useState(user);

  useEffect(() => {
    const t = setInterval(
      () => setQuoteIndex((i) => (i + 1) % quotes.length),
      8000,
    );
    return () => clearInterval(t);
  }, []);

  const handleImageUpload = (e) => {
    const file = e.target.files[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = () => setUser((u) => ({ ...u, avatar: reader.result }));
    reader.readAsDataURL(file);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 via-blue-50/30 to-purple-50/30">
      {/* ================= HERO (UNCHANGED) ================= */}
      <div className="relative h-[380px]">
        <ImageWithFallback
          src={user.cover}
          className="absolute inset-0 w-full h-full object-cover"
        />
        <div className="absolute inset-0 bg-black/40" />

        <div className="relative max-w-7xl mx-auto px-6 h-full flex items-end pb-8">
          <div className="flex gap-6 items-end">
            <div className="relative">
              <Avatar className="size-32 border-4 border-white shadow-xl">
                <AvatarImage src={user.avatar} />
                <AvatarFallback className="text-3xl bg-indigo-600 text-white">
                  AJ
                </AvatarFallback>
              </Avatar>

              <label className="absolute bottom-0 right-0 bg-indigo-600 p-2 rounded-full cursor-pointer">
                <Camera className="size-4 text-white" />
                <input type="file" hidden onChange={handleImageUpload} />
              </label>
            </div>

            <div className="text-white">
              <h1 className="text-3xl font-bold">{user.name}</h1>
              <div className="flex gap-3 mt-2">
                <Badge>
                  <MapPin className="size-3 mr-1" /> {user.location}
                </Badge>
                <Badge>
                  <Calendar className="size-3 mr-1" /> Joined 2024
                </Badge>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* ================= CONTENT ================= */}
      <div className="max-w-7xl mx-auto px-6 py-10 space-y-8">
        {/* ===== MOTIVATION (UNCHANGED) ===== */}
        <Card className="bg-gradient-to-r from-indigo-600 to-purple-600 text-white">
          <CardContent className="p-8">
            <Quote className="size-8 mb-4 opacity-50" />
            <AnimatePresence mode="wait">
              <motion.div
                key={quoteIndex}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
              >
                <p className="text-xl mb-2">"{quotes[quoteIndex].text}"</p>
                <p className="text-white/80">— {quotes[quoteIndex].author}</p>
              </motion.div>
            </AnimatePresence>
          </CardContent>
        </Card>

        {/* ===== PROFILE INFO ===== */}
        <Card>
          <CardHeader className="flex flex-row justify-between">
            <CardTitle>Personal Information</CardTitle>
            {!isEditing ? (
              <Button onClick={() => setIsEditing(true)} size="sm">
                <Edit2 className="size-4 mr-1" /> Edit
              </Button>
            ) : (
              <div className="flex gap-2">
                <Button
                  size="sm"
                  onClick={() => {
                    setUser(tempUser);
                    setIsEditing(false);
                  }}
                >
                  <Save className="size-4 mr-1" /> Save
                </Button>
                <Button
                  size="sm"
                  variant="outline"
                  onClick={() => setIsEditing(false)}
                >
                  <X className="size-4 mr-1" /> Cancel
                </Button>
              </div>
            )}
          </CardHeader>

          <CardContent className="grid md:grid-cols-2 gap-4">
            <div>
              <Label>Name</Label>
              <Input
                value={isEditing ? tempUser.name : user.name}
                disabled={!isEditing}
                onChange={(e) =>
                  setTempUser({ ...tempUser, name: e.target.value })
                }
              />
            </div>
            <div>
              <Label>Email</Label>
              <Input value={user.email} disabled />
            </div>
            <div>
              <Label>Phone</Label>
              <Input
                value={isEditing ? tempUser.phone : user.phone}
                disabled={!isEditing}
                onChange={(e) =>
                  setTempUser({ ...tempUser, phone: e.target.value })
                }
              />
            </div>
            <div>
              <Label>Location</Label>
              <Input
                value={isEditing ? tempUser.location : user.location}
                disabled={!isEditing}
                onChange={(e) =>
                  setTempUser({ ...tempUser, location: e.target.value })
                }
              />
            </div>
          </CardContent>
        </Card>

        {/* ===== PASSWORD ===== */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Shield className="size-5" /> Password & Security
            </CardTitle>
            <CardDescription>Keep your account secure</CardDescription>
          </CardHeader>

          <CardContent className="max-w-md">
            <Label>Current Password</Label>
            <div className="relative">
              <Input type={showPassword ? "text" : "password"} />
              <button
                className="absolute right-3 top-1/2 -translate-y-1/2"
                onClick={() => setShowPassword(!showPassword)}
              >
                {showPassword ? <EyeOff /> : <Eye />}
              </button>
            </div>
          </CardContent>
        </Card>

        {/* ===== GOALS & TASKS ===== */}
        <div className="grid md:grid-cols-2 gap-6">
          <Card>
            <CardContent className="p-6 flex items-center gap-4">
              <Target className="size-10 text-indigo-600" />
              <div>
                <p className="text-2xl font-bold">12</p>
                <p className="text-gray-500">Active Goals</p>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="p-6 flex items-center gap-4">
              <CheckCircle2 className="size-10 text-green-600" />
              <div>
                <p className="text-2xl font-bold">48</p>
                <p className="text-gray-500">Tasks Completed</p>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}
