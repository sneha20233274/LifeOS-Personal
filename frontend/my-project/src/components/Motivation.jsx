import React, { useEffect, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Quote } from "lucide-react";

const QUOTES = [
  {
    text: "The only way to do great work is to love what you do.",
    author: "Steve Jobs",
  },
  {
    text: "Believe you can and you're halfway there.",
    author: "Theodore Roosevelt",
  },
  {
    text: "Success is not final, failure is not fatal: it is the courage to continue that counts.",
    author: "Winston Churchill",
  },
  {
    text: "Discipline is choosing between what you want now and what you want most.",
    author: "Abraham Lincoln",
  },
  {
    text: "Consistency beats motivation when motivation fades.",
    author: "Life OS Principle",
  },
];

export default function Motivation() {
  const [index, setIndex] = useState(0);

  // rotate quotes
  useEffect(() => {
    const interval = setInterval(() => {
      setIndex((prev) => (prev + 1) % QUOTES.length);
    }, 6000);

    return () => clearInterval(interval);
  }, []);

  const current = QUOTES[index];

  return (
    <motion.div
      initial={{ opacity: 0, y: 40 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6, ease: "easeOut" }}
      className="relative overflow-hidden rounded-3xl p-10 md:p-14 text-white shadow-2xl"
    >
      {/* 🔥 Animated Gradient Background */}
      <motion.div
        className="absolute inset-0"
        animate={{
          backgroundPosition: ["0% 50%", "100% 50%", "0% 50%"],
        }}
        transition={{ duration: 20, repeat: Infinity, ease: "linear" }}
        style={{
          backgroundSize: "200% 200%",
          backgroundImage: "linear-gradient(120deg, #0ea5e9, #6366f1, #22d3ee)",
        }}
      />

      {/* Soft Glow */}
      <div className="absolute -top-32 -right-32 w-96 h-96 bg-white/20 rounded-full blur-3xl" />
      <div className="absolute -bottom-32 -left-32 w-96 h-96 bg-indigo-500/20 rounded-full blur-3xl" />

      {/* Content */}
      <div className="relative max-w-3xl">
        <Quote className="w-10 h-10 opacity-70 mb-6" />

        <AnimatePresence mode="wait">
          <motion.div
            key={index}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            transition={{ duration: 0.5 }}
          >
            <p className="text-2xl md:text-3xl font-medium leading-relaxed">
              “{current.text}”
            </p>
            <p className="mt-6 text-white/80 text-lg">— {current.author}</p>
          </motion.div>
        </AnimatePresence>

        {/* Indicators */}
        <div className="flex gap-2 mt-8">
          {QUOTES.map((_, i) => (
            <span
              key={i}
              className={`h-1 rounded-full transition-all ${
                i === index ? "w-8 bg-white" : "w-2 bg-white/40"
              }`}
            />
          ))}
        </div>
      </div>
    </motion.div>
  );
}
