"use client";

import React from "react";
import { Camera, MapPin, Calendar } from "lucide-react";

import Motivation from "./Motivation";
import PersonalInfo from "./PersonalInfo";
import PasswordSecurity from "./PasswordSecurity";
import GoalsTasksTabs from "./GoalsTasksTabs";

import { Avatar, AvatarImage, AvatarFallback } from "./ui/avatar";
import { Badge } from "./ui/badge";
import { ImageWithFallback } from "./figma/ImageWithFallback";

export default function ProfilePage() {
  const user = {
    name: "Alex Johnson",
    location: "San Francisco, CA",
    joined: "Joined 2024",
    avatar: "",
    cover:
      "https://images.unsplash.com/photo-1548126466-4470dfd3a209?fit=crop&w=1600",
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-[#020617] via-[#0f172a] to-[#020617] text-white">
      {/* ================= HERO HEADER ================= */}
      <div className="relative h-[380px]">
        <ImageWithFallback
          src={user.cover}
          alt="Profile cover"
          className="absolute inset-0 w-full h-full object-cover"
        />
        <div className="absolute inset-0 bg-black/60" />

        <div className="relative max-w-7xl mx-auto px-6 h-full flex items-end pb-8">
          <div className="flex items-end gap-6">
            <div className="relative">
              <Avatar className="size-32 border-4 border-indigo-500 shadow-2xl">
                <AvatarImage src={user.avatar} />
                <AvatarFallback className="bg-indigo-600 text-white text-3xl">
                  AJ
                </AvatarFallback>
              </Avatar>

              <label className="absolute bottom-1 right-1 bg-indigo-600 p-2 rounded-full cursor-pointer shadow-lg hover:scale-110 transition">
                <Camera className="size-4 text-white" />
                <input type="file" hidden />
              </label>
            </div>

            <div>
              <h1 className="text-3xl font-bold">{user.name}</h1>
              <div className="flex gap-3 mt-3">
                <Badge className="bg-white/10 text-white">
                  <MapPin className="size-3 mr-1" />
                  {user.location}
                </Badge>
                <Badge className="bg-white/10 text-white">
                  <Calendar className="size-3 mr-1" />
                  {user.joined}
                </Badge>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* ================= PAGE CONTENT ================= */}
      <div className="max-w-7xl mx-auto px-6 py-14 space-y-14">
        <Motivation />

        <PersonalInfo
          user={{
            name: user.name,
            email: "alex@example.com",
            phone: "+1 (555) 123-4567",
            location: user.location,
          }}
          onSave={(updated) => console.log(updated)}
        />

        <div className="grid md:grid-cols-2 gap-12">
          <PasswordSecurity />
          <GoalsTasksTabs goalsCount={12} tasksCount={48} />
        </div>
      </div>
    </div>
  );
}
