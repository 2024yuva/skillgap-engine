"use client";

import Link from "next/link";
import { ArrowRight, Sparkles, Target } from "lucide-react";

export default function FinalCTA() {
  return (
    <section className="py-20 bg-gradient-to-br from-indigo-600 via-purple-600 to-indigo-800 relative overflow-hidden">
      {/* Background decorations */}
      <div className="absolute inset-0 bg-[url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNjAiIGhlaWdodD0iNjAiIHZpZXdCb3g9IjAgMCA2MCA2MCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48ZyBmaWxsPSJub25lIiBmaWxsLXJ1bGU9ImV2ZW5vZGQiPjxnIGZpbGw9IiNmZmZmZmYiIGZpbGwtb3BhY2l0eT0iMC4xIj48Y2lyY2xlIGN4PSIzMCIgY3k9IjMwIiByPSIyIi8+PC9nPjwvZz48L3N2Zz4=')] opacity-20"></div>
      
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
        <div className="text-center">
          <div className="flex items-center justify-center gap-3 mb-6">
            <div className="w-12 h-12 bg-white/20 backdrop-blur-sm rounded-full flex items-center justify-center">
              <Sparkles size={24} className="text-white" />
            </div>
            <div className="w-12 h-12 bg-white/20 backdrop-blur-sm rounded-full flex items-center justify-center">
              <Target size={24} className="text-white" />
            </div>
          </div>
          
          <h2 className="text-4xl lg:text-6xl font-bold text-white leading-tight mb-6">
            Start Building Your<br />
            <span className="bg-gradient-to-r from-yellow-300 to-orange-300 bg-clip-text text-transparent">
              Future Today
            </span>
          </h2>
          
          <p className="text-xl lg:text-2xl text-indigo-100 leading-relaxed mb-12 max-w-4xl mx-auto">
            Understand your skills, improve your resume, discover career opportunities, 
            and create a personalized path toward your goals.
          </p>

          <div className="flex flex-col sm:flex-row gap-6 justify-center mb-16">
            <Link 
              href="/auth" 
              className="inline-flex items-center justify-center px-10 py-5 bg-white text-indigo-600 font-bold text-lg rounded-2xl hover:bg-gray-100 transition-all duration-300 transform hover:scale-105 shadow-xl group"
            >
              Get Started
              <ArrowRight size={24} className="ml-3 group-hover:translate-x-1 transition-transform" />
            </Link>
            
            <Link 
              href="/dashboard" 
              className="inline-flex items-center justify-center px-10 py-5 border-2 border-white/30 text-white font-bold text-lg rounded-2xl hover:bg-white/10 backdrop-blur-sm transition-all duration-300 transform hover:scale-105"
            >
              Explore Skillora
            </Link>
          </div>

          {/* Trust indicators */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8 pt-16 border-t border-white/20">
            <div className="text-center">
              <div className="text-3xl lg:text-4xl font-bold text-white mb-2">10K+</div>
              <div className="text-indigo-200">Success Stories</div>
            </div>
            <div className="text-center">
              <div className="text-3xl lg:text-4xl font-bold text-white mb-2">95%</div>
              <div className="text-indigo-200">Career Growth</div>
            </div>
            <div className="text-center">
              <div className="text-3xl lg:text-4xl font-bold text-white mb-2">500+</div>
              <div className="text-indigo-200">Partner Companies</div>
            </div>
            <div className="text-center">
              <div className="text-3xl lg:text-4xl font-bold text-white mb-2">24/7</div>
              <div className="text-indigo-200">AI Assistant</div>
            </div>
          </div>
        </div>
      </div>

      {/* Floating elements */}
      <div className="absolute top-1/4 left-10 w-20 h-20 bg-white/10 rounded-full animate-float"></div>
      <div className="absolute top-1/3 right-16 w-16 h-16 bg-purple-300/20 rounded-full animate-float-delay"></div>
      <div className="absolute bottom-1/4 left-1/4 w-12 h-12 bg-yellow-300/20 rounded-full animate-bounce"></div>
      <div className="absolute bottom-1/3 right-1/4 w-14 h-14 bg-indigo-300/20 rounded-full animate-pulse"></div>

      <style jsx>{`
        @keyframes float {
          0%, 100% { transform: translateY(0px); }
          50% { transform: translateY(-20px); }
        }
        
        @keyframes float-delay {
          0%, 100% { transform: translateY(0px); }
          50% { transform: translateY(-15px); }
        }
        
        .animate-float {
          animation: float 6s ease-in-out infinite;
        }
        
        .animate-float-delay {
          animation: float-delay 4s ease-in-out infinite 2s;
        }
      `}</style>
    </section>
  );
}