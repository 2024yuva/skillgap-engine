"use client";

import { Target, DollarSign, CheckCircle, X, ArrowRight } from "lucide-react";
import Link from "next/link";

const jobCards = [
  {
    title: "Embedded Systems Engineer",
    match: 82,
    salary: "₹5–10 LPA",
    matchingSkills: ["C Programming", "Microcontrollers", "Electronics"],
    missingSkills: ["RTOS", "Embedded Linux"],
    color: "bg-green-50 border-green-200"
  },
  {
    title: "Data Analyst",
    match: 76,
    salary: "₹4–8 LPA", 
    matchingSkills: ["Python", "Excel", "Statistics"],
    missingSkills: ["SQL", "Power BI"],
    color: "bg-blue-50 border-blue-200"
  },
  {
    title: "Electrical Design Engineer",
    match: 88,
    salary: "₹4–9 LPA",
    matchingSkills: ["AutoCAD", "Electrical Systems", "Circuit Design"],
    missingSkills: ["Advanced Electrical Design"],
    color: "bg-purple-50 border-purple-200"
  }
];

export default function JobMatching() {
  return (
    <section className="py-20 bg-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="text-3xl lg:text-4xl font-bold text-gray-900 mb-4">
            Find Jobs That Match Your Skills
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Discover career opportunities tailored to your current skills and get insights 
            on what you need to learn to land your dream job.
          </p>
        </div>

        <div className="grid lg:grid-cols-3 gap-8 mb-12">
          {jobCards.map((job, index) => (
            <div 
              key={index}
              className={`${job.color} rounded-2xl p-6 border-2 hover:shadow-xl transition-all duration-300 group hover:scale-105`}
            >
              {/* Header */}
              <div className="mb-6">
                <h3 className="text-xl font-bold text-gray-900 mb-3">
                  {job.title}
                </h3>
                
                <div className="flex items-center gap-4 mb-3">
                  <div className="flex items-center gap-2">
                    <Target size={16} className="text-green-600" />
                    <span className="font-bold text-green-600">{job.match}% Match</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <DollarSign size={16} className="text-blue-600" />
                    <span className="font-bold text-blue-600">{job.salary}</span>
                  </div>
                </div>
              </div>

              {/* Skills */}
              <div className="space-y-4">
                <div>
                  <h4 className="text-sm font-semibold text-gray-700 mb-2 flex items-center gap-2">
                    <CheckCircle size={14} className="text-green-600" />
                    Matching Skills:
                  </h4>
                  <div className="flex flex-wrap gap-2">
                    {job.matchingSkills.map((skill, skillIndex) => (
                      <span 
                        key={skillIndex}
                        className="bg-green-100 text-green-700 px-2 py-1 rounded-lg text-xs font-medium"
                      >
                        {skill}
                      </span>
                    ))}
                  </div>
                </div>

                <div>
                  <h4 className="text-sm font-semibold text-gray-700 mb-2 flex items-center gap-2">
                    <X size={14} className="text-orange-600" />
                    Missing Skills:
                  </h4>
                  <div className="flex flex-wrap gap-2">
                    {job.missingSkills.map((skill, skillIndex) => (
                      <span 
                        key={skillIndex}
                        className="bg-orange-100 text-orange-700 px-2 py-1 rounded-lg text-xs font-medium"
                      >
                        {skill}
                      </span>
                    ))}
                  </div>
                </div>
              </div>

              {/* Match Progress */}
              <div className="mt-6 pt-4 border-t border-gray-200">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-sm font-medium text-gray-700">Match Score</span>
                  <span className="text-sm font-bold text-gray-900">{job.match}%</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div 
                    className="bg-gradient-to-r from-green-500 to-blue-500 h-2 rounded-full transition-all duration-500" 
                    style={{ width: `${job.match}%` }}
                  ></div>
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* CTA */}
        <div className="text-center">
          <Link 
            href="/courses"
            className="inline-flex items-center justify-center px-8 py-4 bg-indigo-600 text-white font-semibold rounded-xl hover:bg-indigo-700 transition-colors group"
          >
            Explore Jobs
            <ArrowRight size={20} className="ml-2 group-hover:translate-x-1 transition-transform" />
          </Link>
        </div>

        {/* Additional Info */}
        <div className="mt-16 grid md:grid-cols-3 gap-8">
          <div className="text-center">
            <div className="w-16 h-16 bg-indigo-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <Target size={24} className="text-indigo-600" />
            </div>
            <h3 className="text-lg font-bold text-gray-900 mb-2">Smart Matching</h3>
            <p className="text-gray-600 text-sm">
              Our AI analyzes job descriptions and matches them with your skill profile
            </p>
          </div>

          <div className="text-center">
            <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <CheckCircle size={24} className="text-green-600" />
            </div>
            <h3 className="text-lg font-bold text-gray-900 mb-2">Real-time Data</h3>
            <p className="text-gray-600 text-sm">
              Updated daily with the latest job market trends and salary information
            </p>
          </div>

          <div className="text-center">
            <div className="w-16 h-16 bg-purple-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <DollarSign size={24} className="text-purple-600" />
            </div>
            <h3 className="text-lg font-bold text-gray-900 mb-2">Salary Insights</h3>
            <p className="text-gray-600 text-sm">
              Get accurate salary ranges based on your skills and market demand
            </p>
          </div>
        </div>
      </div>
    </section>
  );
}