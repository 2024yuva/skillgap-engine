"use client";

import { Target, AlertTriangle, DollarSign, TrendingUp, Clock } from "lucide-react";

const insights = [
  {
    icon: Target,
    label: "Career Match",
    value: "Embedded Engineer — 82% Match",
    color: "bg-green-50 border-green-200 text-green-600"
  },
  {
    icon: AlertTriangle,
    label: "Skill Gap",
    value: "Missing: RTOS, Embedded Linux",
    color: "bg-orange-50 border-orange-200 text-orange-600"
  },
  {
    icon: DollarSign,
    label: "Salary Insight",
    value: "₹5 – ₹10 LPA",
    color: "bg-blue-50 border-blue-200 text-blue-600"
  },
  {
    icon: TrendingUp,
    label: "Career Growth",
    value: "High Growth Potential",
    color: "bg-purple-50 border-purple-200 text-purple-600"
  },
  {
    icon: Clock,
    label: "Learning Duration",
    value: "Estimated: 3–5 Months",
    color: "bg-indigo-50 border-indigo-200 text-indigo-600"
  }
];

export default function CareerInsights() {
  return (
    <section className="py-20 bg-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="text-3xl lg:text-4xl font-bold text-gray-900 mb-4">
            Know Where You Stand. Know What Comes Next.
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Get comprehensive insights about your career position, skill gaps, and growth opportunities 
            with our AI-powered analysis.
          </p>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-5 gap-6 mb-16">
          {insights.map((insight, index) => {
            const Icon = insight.icon;
            return (
              <div 
                key={index}
                className={`${insight.color} rounded-2xl p-6 border-2 hover:shadow-xl transition-all duration-300 group hover:scale-105`}
              >
                <div className="flex items-center gap-3 mb-4">
                  <Icon size={20} />
                  <span className="text-sm font-medium text-gray-700">{insight.label}</span>
                </div>
                <p className="font-bold text-gray-900 group-hover:scale-105 transition-transform duration-300">
                  {insight.value}
                </p>
              </div>
            );
          })}
        </div>

        {/* Interactive Dashboard Preview */}
        <div className="bg-gradient-to-br from-gray-50 to-indigo-50 rounded-3xl p-8 lg:p-12 border-2 border-indigo-100">
          <div className="grid lg:grid-cols-2 gap-8 items-center">
            <div>
              <h3 className="text-2xl lg:text-3xl font-bold text-gray-900 mb-4">
                Real-time Career Intelligence
              </h3>
              <p className="text-lg text-gray-600 mb-6 leading-relaxed">
                Our AI continuously analyzes market trends, salary data, and job requirements 
                to provide you with the most current career insights and recommendations.
              </p>
              
              <div className="space-y-4">
                <div className="flex items-center gap-3">
                  <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
                  <span className="text-gray-700">Live job market analysis</span>
                </div>
                <div className="flex items-center gap-3">
                  <div className="w-2 h-2 bg-blue-500 rounded-full animate-pulse"></div>
                  <span className="text-gray-700">Updated salary benchmarks</span>
                </div>
                <div className="flex items-center gap-3">
                  <div className="w-2 h-2 bg-purple-500 rounded-full animate-pulse"></div>
                  <span className="text-gray-700">Skill demand forecasting</span>
                </div>
              </div>
            </div>

            <div className="relative">
              {/* Mock Dashboard */}
              <div className="bg-white rounded-2xl shadow-xl p-6 border">
                <div className="flex items-center justify-between mb-4">
                  <h4 className="font-semibold text-gray-900">Market Analysis</h4>
                  <div className="w-3 h-3 bg-green-500 rounded-full animate-pulse"></div>
                </div>
                
                <div className="space-y-3">
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-gray-600">Job Demand</span>
                    <div className="flex items-center gap-2">
                      <div className="w-20 h-2 bg-gray-200 rounded-full">
                        <div className="w-16 h-2 bg-green-500 rounded-full"></div>
                      </div>
                      <span className="text-sm font-medium">High</span>
                    </div>
                  </div>
                  
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-gray-600">Salary Growth</span>
                    <div className="flex items-center gap-2">
                      <div className="w-20 h-2 bg-gray-200 rounded-full">
                        <div className="w-14 h-2 bg-blue-500 rounded-full"></div>
                      </div>
                      <span className="text-sm font-medium">+12%</span>
                    </div>
                  </div>
                  
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-gray-600">Skill Match</span>
                    <div className="flex items-center gap-2">
                      <div className="w-20 h-2 bg-gray-200 rounded-full">
                        <div className="w-16 h-2 bg-purple-500 rounded-full"></div>
                      </div>
                      <span className="text-sm font-medium">82%</span>
                    </div>
                  </div>
                </div>
              </div>

              {/* Floating elements */}
              <div className="absolute -top-4 -right-4 w-12 h-12 bg-indigo-100 rounded-full flex items-center justify-center animate-bounce">
                <TrendingUp size={16} className="text-indigo-600" />
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}