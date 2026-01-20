"use client";

import React from "react";
import { useDispatch } from "react-redux";
import { useNavigate } from "react-router-dom";
import { logout } from "../store/authSlice";

import { Camera, MapPin, Calendar } from "lucide-react";

import Motivation from "./Motivation";
import PersonalInfo from "./PersonalInfo";
import PasswordSecurity from "./PasswordSecurity";
import GoalsTasksTabs from "./GoalsTasksTabs";
import { useChangePasswordMutation } from "../services/authApi";

import { Avatar, AvatarImage, AvatarFallback } from "./ui/avatar";
import { Badge } from "./ui/badge";
import { ImageWithFallback } from "./figma/ImageWithFallback";

// 🔑 profile API
import { useGetMyProfileQuery } from "../services/userApi";

export default function ProfilePage() {
  const { data: user, isLoading } = useGetMyProfileQuery();
  const [changePassword] = useChangePasswordMutation();
  const navigate = useNavigate();
  const dispatch = useDispatch();

  // while profile loads (NO WHITE FLASH)
  if (isLoading || !user) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-[#020617] via-[#0f172a] to-[#020617] text-white flex items-center justify-center">
        <p className="text-gray-400">Loading profile…</p>
      </div>
    );
  }

  function formatJoinedDate(dateString) {
    if (!dateString) return "";

    return new Date(dateString).toLocaleDateString("en-US", {
      month: "long",
      year: "numeric",
    });
  }


  return (
    <div className="min-h-screen bg-gradient-to-br from-[#020617] via-[#0f172a] to-[#020617] text-white">
      {/* ================= HERO HEADER ================= */}
      <div className="relative h-[380px]">
        <ImageWithFallback
          src={
            user.cover ||
            "https://images.unsplash.com/photo-1548126466-4470dfd3a209?fit=crop&w=1600"
          }
          alt="Profile cover"
          className="absolute inset-0 w-full h-full object-cover"
        />

        <div className="absolute inset-0 bg-black/60" />

        <div className="relative max-w-7xl mx-auto px-6 h-full flex items-end pb-8">
          <div className="flex items-end gap-6">
            {/* Avatar */}
            <div className="relative">
              <Avatar className="size-32 border-4 border-indigo-500 shadow-2xl">
                <AvatarImage src={user.avatar || ""} />
                <AvatarFallback className="bg-indigo-600 text-white text-3xl">
                  {user.first_name?.[0]}
                  {user.last_name?.[0]}
                </AvatarFallback>
              </Avatar>

              <label className="absolute bottom-1 right-1 bg-indigo-600 p-2 rounded-full cursor-pointer shadow-lg hover:scale-110 transition">
                <Camera className="size-4 text-white" />
                <input type="file" hidden />
              </label>
            </div>

            {/* User Info */}
            <div>
              <h1 className="text-3xl font-bold">
                {user.first_name} {user.last_name}
              </h1>

              <div className="flex gap-3 mt-3">
                {user.location && (
                  <Badge className="bg-white/10 text-white">
                    <MapPin className="size-3 mr-1" />
                    {user.location}
                  </Badge>
                )}

                <Badge className="bg-white/10 text-white">
                  <Calendar className="size-3 mr-1" />
                  Joined {formatJoinedDate(user.created_at)}
                </Badge>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* ================= PAGE CONTENT ================= */}
      <div className="max-w-7xl mx-auto px-6 py-14 space-y-14">
        {/* 🔥 Motivation */}
        <Motivation />

        {/* 🧍 Personal Info */}
        <PersonalInfo user={user} />

        {/* 🔐 Password + 🎯 Goals */}
        <div className="grid md:grid-cols-2 gap-12">
          <PasswordSecurity
            onUpdate={async (form) => {
              try {
                await changePassword(form).unwrap();
                dispatch(logout());
                navigate("/login");
                alert("Password updated successfully");
              } catch (err) {
                alert(err?.data?.detail || "Password update failed");
              }
            }}
          />
          <GoalsTasksTabs goalsCount={12} tasksCount={48} />
        </div>
      </div>
    </div>
  );
}
