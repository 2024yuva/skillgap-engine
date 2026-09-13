"use client";

import { MessageCircle, Sparkles, ArrowRight } from "lucide-react";
import Link from "next/link";

const exampleQuestions = [
  "How can I improve my resume?",
  "What jobs are suitable for my skills?",
  "What skills should I learn next?",
  "What salary can I expect?",
  "Show my skill gap analysis."
];

export default function SkilloraAI() {
  return (
    <section className="py-20 bg-gradient-to-br from-indigo-50 to-purple-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid lg:grid-cols-2 gap-12 items-center">
          {/* Left Content */}
          <div>
            <div className="flex items-center gap-3 mb-6">
              <div className="w-12 h-12 bg-indigo-600 rounded-full flex items-center justify-center">
                <MessageCircle size={24} className="text-white" />
              </div>
              <h2 className="text-3xl lg:text-4xl font-bold text-gray-900">
                Meet Skillora AI
              </h2>
            </div>
            
            <p className="text-xl text-gray-600 leading-relaxed mb-8">
              Your intelligent career assistant, available whenever you need guidance. 
              Get instant answers, personalized advice, and actionable insights 24/7.
            </p>

            <div className="space-y-3 mb-8">
              {exampleQuestions.map((question, index) => (
                <div 
                  key={index}
                  className="flex items-center gap-3 p-3 bg-white rounded-lg border border-indigo-100 hover:border-indigo-300 transition-colors group cursor-pointer"
                >
                  <Sparkles size={16} className="text-indigo-600 flex-shrink-0" />
                  <span className="text-gray-700 group-hover:text-indigo-700 transition-colors">
                    {question}
                  </span>
                </div>
              ))}
            </div>

            <Link 
              href="/auth"
              className="inline-flex items-center justify-center px-8 py-4 bg-indigo-600 text-white font-semibold rounded-xl hover:bg-indigo-700 transition-colors group"
            >
              Ask Skillora AI
              <ArrowRight size={20} className="ml-2 group-hover:translate-x-1 transition-transform" />
            </Link>
          </div>

          {/* Right Chat Preview */}
          <div className="relative">
            <div className="bg-white rounded-2xl shadow-2xl border border-gray-200 overflow-hidden">
              {/* Chat Header */}
              <div className="bg-indigo-600 p-4">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 bg-white/20 rounded-full flex items-center justify-center">
                    <MessageCircle size={20} className="text-white" />
                  </div>
                  <div>
                    <h3 className="text-white font-bold">Skillora AI Assistant</h3>
                    <p className="text-indigo-200 text-sm">Your Personal Career & Skill Guide</p>
                  </div>
                  <div className="ml-auto">
                    <div className="w-3 h-3 bg-green-400 rounded-full animate-pulse"></div>
                  </div>
                </div>
              </div>

              {/* Chat Messages */}
              <div className="p-4 h-80 overflow-y-auto space-y-4">
                {/* AI Welcome Message */}
                <div className="flex gap-3">
                  <div className="w-8 h-8 bg-indigo-100 rounded-full flex items-center justify-center flex-shrink-0">
                    <MessageCircle size={14} className="text-indigo-600" />
                  </div>
                  <div className="bg-gray-100 rounded-2xl rounded-tl-sm p-3 max-w-xs">
                    <p className="text-gray-800 text-sm">
                      Hi! I'm Skillora AI 👋 I can help you improve your resume, identify skill gaps, 
                      discover suitable job roles, and build your personalized learning path.
                    </p>
                  </div>
                </div>

                {/* User Message */}
                <div className="flex gap-3 justify-end">
                  <div className="bg-indigo-600 rounded-2xl rounded-tr-sm p-3 max-w-xs">
                    <p className="text-white text-sm">
                      What jobs are suitable for my skills?
                    </p>
                  </div>
                  <div className="w-8 h-8 bg-gray-200 rounded-full flex items-center justify-center flex-shrink-0">
                    <span className="text-gray-600 text-xs font-bold">You</span>
                  </div>
                </div>

                {/* AI Response */}
                <div className="flex gap-3">
                  <div className="w-8 h-8 bg-indigo-100 rounded-full flex items-center justify-center flex-shrink-0">
                    <MessageCircle size={14} className="text-indigo-600" />
                  </div>
                  <div className="bg-gray-100 rounded-2xl rounded-tl-sm p-3 max-w-xs">
                    <p className="text-gray-800 text-sm mb-2">
                      Based on your profile, here are the top matching roles:
                    </p>
                    <div className="space-y-2">
                      <div className="bg-white rounded-lg p-2 border">
                        <div className="text-xs font-bold text-green-600">82% Match</div>
                        <div className="text-xs text-gray-800">Embedded Systems Engineer</div>
                      </div>
                      <div className="bg-white rounded-lg p-2 border">
                        <div className="text-xs font-bold text-blue-600">76% Match</div>
                        <div className="text-xs text-gray-800">Data Analyst</div>
                      </div>
                    </div>
                  </div>
                </div>

                {/* Typing indicator */}
                <div className="flex gap-3">
                  <div className="w-8 h-8 bg-indigo-100 rounded-full flex items-center justify-center flex-shrink-0">
                    <MessageCircle size={14} className="text-indigo-600" />
                  </div>
                  <div className="bg-gray-100 rounded-2xl rounded-tl-sm p-3">
                    <div className="flex space-x-1">
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                    </div>
                  </div>
                </div>
              </div>

              {/* Chat Input */}
              <div className="border-t border-gray-200 p-4">
                <div className="flex gap-2">
                  <input 
                    type="text" 
                    placeholder="Ask anything about your career..."
                    className="flex-1 bg-gray-100 rounded-lg px-3 py-2 text-sm border-0 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                    disabled
                  />
                  <button className="bg-indigo-600 text-white p-2 rounded-lg hover:bg-indigo-700 transition-colors">
                    <ArrowRight size={16} />
                  </button>
                </div>
              </div>
            </div>

            {/* Floating elements */}
            <div className="absolute -top-4 -right-4 w-12 h-12 bg-purple-100 rounded-full flex items-center justify-center animate-bounce">
              <Sparkles size={16} className="text-purple-600" />
            </div>
            <div className="absolute -bottom-4 -left-4 w-10 h-10 bg-indigo-100 rounded-full flex items-center justify-center animate-pulse">
              <MessageCircle size={14} className="text-indigo-600" />
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}