"use client";

import { Upload, CheckCircle, FileText, ArrowRight } from "lucide-react";
import Link from "next/link";

const recommendations = [
  "Add relevant technical skills",
  "Highlight projects and achievements", 
  "Improve ATS-friendly keywords",
  "Use strong action-oriented language",
  "Maintain a clear professional format"
];

export default function ResumePreview() {
  return (
    <section className="py-20 bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="text-3xl lg:text-4xl font-bold text-gray-900 mb-4">
            Build a Stronger Resume
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Analyze your resume and receive intelligent recommendations to improve your skills, 
            keywords, projects, achievements, and overall career presentation.
          </p>
        </div>

        <div className="grid lg:grid-cols-2 gap-12 items-center">
          {/* Upload Area */}
          <div>
            <div className="bg-white rounded-2xl p-8 border-2 border-dashed border-gray-300 hover:border-indigo-400 transition-colors group">
              <div className="text-center">
                <div className="w-16 h-16 bg-indigo-100 rounded-full flex items-center justify-center mx-auto mb-6 group-hover:bg-indigo-200 transition-colors">
                  <Upload size={24} className="text-indigo-600" />
                </div>
                
                <h3 className="text-xl font-bold text-gray-900 mb-2">
                  Upload Your Resume
                </h3>
                
                <p className="text-gray-600 mb-6">
                  Supported formats:
                </p>
                
                <div className="flex items-center justify-center gap-4 mb-6">
                  <span className="bg-red-100 text-red-600 px-3 py-1 rounded-lg text-sm font-medium">PDF</span>
                  <span className="bg-blue-100 text-blue-600 px-3 py-1 rounded-lg text-sm font-medium">DOCX</span>
                  <span className="bg-green-100 text-green-600 px-3 py-1 rounded-lg text-sm font-medium">TXT</span>
                </div>
                
                <Link 
                  href="/dashboard"
                  className="inline-flex items-center justify-center px-6 py-3 bg-indigo-600 text-white font-semibold rounded-xl hover:bg-indigo-700 transition-colors group"
                >
                  <FileText size={18} className="mr-2" />
                  Analyze Resume
                  <ArrowRight size={18} className="ml-2 group-hover:translate-x-1 transition-transform" />
                </Link>
              </div>
            </div>

            {/* Features */}
            <div className="mt-8 grid grid-cols-2 gap-4">
              <div className="bg-white rounded-xl p-4 border border-gray-200">
                <div className="text-center">
                  <div className="text-2xl font-bold text-indigo-600 mb-1">AI</div>
                  <div className="text-sm text-gray-600">Powered Analysis</div>
                </div>
              </div>
              <div className="bg-white rounded-xl p-4 border border-gray-200">
                <div className="text-center">
                  <div className="text-2xl font-bold text-green-600 mb-1">ATS</div>
                  <div className="text-sm text-gray-600">Friendly Format</div>
                </div>
              </div>
            </div>
          </div>

          {/* Recommendations Preview */}
          <div>
            <div className="bg-white rounded-2xl p-8 border border-gray-200 shadow-xl">
              <div className="flex items-center gap-3 mb-6">
                <CheckCircle size={24} className="text-green-600" />
                <h3 className="text-xl font-bold text-gray-900">
                  AI Recommendations
                </h3>
              </div>

              <div className="space-y-4">
                {recommendations.map((recommendation, index) => (
                  <div 
                    key={index}
                    className="flex items-start gap-3 p-4 bg-gray-50 rounded-xl hover:bg-indigo-50 transition-colors group"
                  >
                    <div className="w-6 h-6 bg-indigo-100 rounded-full flex items-center justify-center flex-shrink-0 mt-0.5 group-hover:bg-indigo-200 transition-colors">
                      <span className="text-indigo-600 text-sm font-bold">{index + 1}</span>
                    </div>
                    <p className="text-gray-700 group-hover:text-indigo-700 transition-colors">
                      {recommendation}
                    </p>
                  </div>
                ))}
              </div>

              {/* Score Preview */}
              <div className="mt-6 p-4 bg-gradient-to-r from-indigo-50 to-purple-50 rounded-xl border border-indigo-200">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-sm font-medium text-gray-700">Resume Score</span>
                  <span className="text-sm text-indigo-600 font-bold">82/100</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div className="bg-gradient-to-r from-indigo-600 to-purple-600 h-2 rounded-full" style={{ width: '82%' }}></div>
                </div>
                <p className="text-xs text-gray-600 mt-2">
                  Great start! Follow our recommendations to reach 95+
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}