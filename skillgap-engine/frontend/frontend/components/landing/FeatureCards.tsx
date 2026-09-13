"use client";

import { FileText, Brain, BarChart3, Briefcase, BookOpen } from "lucide-react";

const features = [
  {
    icon: FileText,
    title: "Resume Builder & Analysis",
    description: "Create and improve professional, ATS-friendly resumes with intelligent recommendations.",
    color: "bg-blue-50 border-blue-200 text-blue-600"
  },
  {
    icon: Brain,
    title: "Skill Analysis", 
    description: "Understand your current technical and professional skills through structured competency analysis.",
    color: "bg-purple-50 border-purple-200 text-purple-600"
  },
  {
    icon: BarChart3,
    title: "Skill Gap Detection",
    description: "Identify missing skills required for your target career role.",
    color: "bg-green-50 border-green-200 text-green-600"
  },
  {
    icon: Briefcase,
    title: "Smart Job Matching",
    description: "Discover suitable job roles based on your skills and calculate your career match percentage.",
    color: "bg-orange-50 border-orange-200 text-orange-600"
  },
  {
    icon: BookOpen,
    title: "Personalized Learning Path",
    description: "Receive recommendations for what skills to learn next and how to improve your career readiness.",
    color: "bg-indigo-50 border-indigo-200 text-indigo-600"
  }
];

export default function FeatureCards() {
  return (
    <section className="py-20 bg-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="text-3xl lg:text-4xl font-bold text-gray-900 mb-4">
            Everything You Need for Career Growth
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Our comprehensive AI-powered platform provides all the tools and insights 
            you need to advance your career.
          </p>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
          {features.map((feature, index) => {
            const Icon = feature.icon;
            return (
              <div 
                key={index}
                className="bg-white rounded-2xl p-8 border-2 border-gray-100 hover:border-indigo-200 hover:shadow-xl transition-all duration-300 group"
              >
                <div className={`w-14 h-14 rounded-xl ${feature.color} flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300`}>
                  <Icon size={24} />
                </div>
                
                <h3 className="text-xl font-bold text-gray-900 mb-4 group-hover:text-indigo-600 transition-colors">
                  {feature.title}
                </h3>
                
                <p className="text-gray-600 leading-relaxed">
                  {feature.description}
                </p>
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
}