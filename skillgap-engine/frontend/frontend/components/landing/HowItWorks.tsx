"use client";

import { Upload, Brain, Target, TrendingUp, ArrowRight } from "lucide-react";

const steps = [
  {
    icon: Upload,
    title: "Upload Your Resume",
    description: "Simply upload your resume or create a profile. Our AI instantly analyzes your skills and experience.",
    color: "bg-blue-600"
  },
  {
    icon: Brain,
    title: "AI Skill Analysis", 
    description: "Our intelligent system identifies your technical skills, soft skills, and competency levels.",
    color: "bg-purple-600"
  },
  {
    icon: Target,
    title: "Choose Target Role",
    description: "Select your dream job role and get personalized insights about skill gaps and requirements.",
    color: "bg-green-600"
  },
  {
    icon: TrendingUp,
    title: "Get Career Roadmap",
    description: "Receive personalized job recommendations, salary insights, and a structured learning path.",
    color: "bg-orange-600"
  }
];

export default function HowItWorks() {
  return (
    <section className="py-20 bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="text-3xl lg:text-4xl font-bold text-gray-900 mb-4">
            Your Career Journey in Four Simple Steps
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Get personalized job recommendations, salary insights, and a structured learning path 
            tailored specifically for your goals.
          </p>
        </div>

        {/* Desktop Timeline */}
        <div className="hidden lg:block">
          <div className="relative">
            {/* Timeline line */}
            <div className="absolute top-1/2 left-0 w-full h-1 bg-gray-200 transform -translate-y-1/2"></div>
            <div className="absolute top-1/2 left-0 w-3/4 h-1 bg-indigo-600 transform -translate-y-1/2 transition-all duration-1000"></div>
            
            <div className="grid grid-cols-4 gap-8 relative z-10">
              {steps.map((step, index) => {
                const Icon = step.icon;
                return (
                  <div key={index} className="text-center">
                    {/* Icon */}
                    <div className={`w-16 h-16 mx-auto ${step.color} rounded-full flex items-center justify-center mb-6 shadow-lg`}>
                      <Icon size={28} className="text-white" />
                    </div>
                    
                    {/* Content */}
                    <div className="bg-white rounded-xl p-6 shadow-lg border">
                      <h3 className="text-lg font-bold text-gray-900 mb-3">
                        {step.title}
                      </h3>
                      <p className="text-gray-600 text-sm leading-relaxed">
                        {step.description}
                      </p>
                    </div>
                    
                    {/* Arrow */}
                    {index < steps.length - 1 && (
                      <div className="absolute top-8 right-0 transform translate-x-1/2 translate-y-1/2">
                        <ArrowRight size={20} className="text-indigo-600" />
                      </div>
                    )}
                  </div>
                );
              })}
            </div>
          </div>
        </div>

        {/* Mobile Timeline */}
        <div className="lg:hidden space-y-8">
          {steps.map((step, index) => {
            const Icon = step.icon;
            return (
              <div key={index} className="flex gap-4">
                <div className={`w-12 h-12 ${step.color} rounded-full flex items-center justify-center flex-shrink-0 shadow-lg`}>
                  <Icon size={20} className="text-white" />
                </div>
                
                <div className="flex-1">
                  <h3 className="text-lg font-bold text-gray-900 mb-2">
                    {step.title}
                  </h3>
                  <p className="text-gray-600 leading-relaxed">
                    {step.description}
                  </p>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
}