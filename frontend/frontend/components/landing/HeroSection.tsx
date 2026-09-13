"use client";

import Link from "next/link";
import { ArrowRight, Target, TrendingUp, Users, Award, BookOpen, Zap } from "lucide-react";

export default function HeroSection() {
  return (
    <section className="py-20 lg:py-32 bg-gradient-to-br from-gray-50 to-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid lg:grid-cols-2 gap-12 items-center">
          {/* Left Content */}
          <div>
            <h1 className="text-4xl lg:text-6xl font-bold text-gray-900 leading-tight mb-6">
              Build Your Skills.{" "}
              <span className="text-indigo-600">Strengthen Your Resume.</span>{" "}
              Shape Your Career.
            </h1>
            
            <p className="text-xl text-gray-600 leading-relaxed mb-8">
              Skillora uses intelligent skill analysis to help you understand your strengths, 
              identify skill gaps, improve your resume, discover suitable jobs, and build a 
              personalized career path.
            </p>

            <div className="flex flex-col sm:flex-row gap-4 mb-12">
              <Link 
                href="/auth" 
                className="inline-flex items-center justify-center px-8 py-4 bg-indigo-600 text-white font-semibold rounded-xl hover:bg-indigo-700 transition-colors group"
              >
                Get Started
                <ArrowRight size={20} className="ml-2 group-hover:translate-x-1 transition-transform" />
              </Link>
              <Link 
                href="/dashboard" 
                className="inline-flex items-center justify-center px-8 py-4 border-2 border-gray-300 text-gray-700 font-semibold rounded-xl hover:border-indigo-600 hover:text-indigo-600 transition-colors"
              >
                Analyze My Resume
              </Link>
            </div>

            {/* Trust indicators */}
            <div className="flex items-center gap-8 text-sm text-gray-500">
              <div className="flex items-center gap-2">
                <Users size={16} />
                <span>10,000+ users</span>
              </div>
              <div className="flex items-center gap-2">
                <Award size={16} />
                <span>AI-powered analysis</span>
              </div>
              <div className="flex items-center gap-2">
                <Zap size={16} />
                <span>Instant insights</span>
              </div>
            </div>
          </div>

          {/* Right Dashboard Preview */}
          <div className="relative">
            {/* Background decoration */}
            <div className="absolute inset-0 bg-gradient-to-r from-indigo-600/10 to-purple-600/10 rounded-3xl blur-3xl"></div>
            
            <div className="relative bg-white rounded-2xl shadow-2xl p-6 border">
              {/* Dashboard Header */}
              <div className="flex items-center justify-between mb-6">
                <h3 className="text-lg font-semibold text-gray-900">Career Dashboard</h3>
                <div className="w-3 h-3 bg-green-500 rounded-full animate-pulse"></div>
              </div>

              {/* Dashboard Cards */}
              <div className="grid grid-cols-2 gap-4 mb-6">
                <div className="bg-gradient-to-r from-indigo-50 to-indigo-100 rounded-xl p-4 border border-indigo-200">
                  <div className="flex items-center gap-2 mb-2">
                    <Target size={16} className="text-indigo-600" />
                    <span className="text-sm font-medium text-gray-700">Resume Score</span>
                  </div>
                  <p className="text-2xl font-bold text-indigo-600">82/100</p>
                </div>

                <div className="bg-gradient-to-r from-green-50 to-green-100 rounded-xl p-4 border border-green-200">
                  <div className="flex items-center gap-2 mb-2">
                    <TrendingUp size={16} className="text-green-600" />
                    <span className="text-sm font-medium text-gray-700">Career Match</span>
                  </div>
                  <p className="text-2xl font-bold text-green-600">85%</p>
                </div>

                <div className="bg-gradient-to-r from-purple-50 to-purple-100 rounded-xl p-4 border border-purple-200">
                  <div className="flex items-center gap-2 mb-2">
                    <BookOpen size={16} className="text-purple-600" />
                    <span className="text-sm font-medium text-gray-700">Skills Found</span>
                  </div>
                  <p className="text-2xl font-bold text-purple-600">12</p>
                </div>

                <div className="bg-gradient-to-r from-orange-50 to-orange-100 rounded-xl p-4 border border-orange-200">
                  <div className="flex items-center gap-2 mb-2">
                    <Award size={16} className="text-orange-600" />
                    <span className="text-sm font-medium text-gray-700">Skill Gaps</span>
                  </div>
                  <p className="text-2xl font-bold text-orange-600">4</p>
                </div>
              </div>

              {/* Recommended Role */}
              <div className="bg-gradient-to-r from-gray-50 to-gray-100 rounded-xl p-4 border">
                <h4 className="font-semibold text-gray-900 mb-2">Recommended Role</h4>
                <p className="text-lg font-medium text-indigo-600 mb-1">Embedded Systems Engineer</p>
                <p className="text-sm text-gray-600">Expected Salary: ₹5 – ₹10 LPA</p>
              </div>
            </div>

            {/* Floating elements */}
            <div className="absolute -top-4 -right-4 w-20 h-20 bg-indigo-100 rounded-full flex items-center justify-center animate-bounce">
              <Target size={24} className="text-indigo-600" />
            </div>
            <div className="absolute -bottom-4 -left-4 w-16 h-16 bg-purple-100 rounded-full flex items-center justify-center animate-pulse">
              <TrendingUp size={20} className="text-purple-600" />
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}