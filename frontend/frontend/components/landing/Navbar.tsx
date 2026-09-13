"use client";

import { useState } from "react";
import Link from "next/link";
import { Menu, X, Brain } from "lucide-react";

export default function Navbar() {
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  return (
    <nav className="sticky top-0 z-50 bg-white/95 backdrop-blur-sm border-b border-gray-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <div className="flex items-center">
            <Link href="/" className="flex items-center gap-2">
              <div className="w-8 h-8 rounded-lg bg-indigo-600 flex items-center justify-center">
                <Brain size={18} className="text-white" />
              </div>
              <div>
                <span className="text-xl font-bold text-gray-900">Skillora</span>
                <p className="text-xs text-gray-500 hidden sm:block">AI Career Intelligence</p>
              </div>
            </Link>
          </div>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center space-x-8">
            <Link href="/" className="text-gray-700 hover:text-indigo-600 font-medium transition-colors">
              Home
            </Link>
            <Link href="/dashboard" className="text-gray-700 hover:text-indigo-600 font-medium transition-colors">
              Resume
            </Link>
            <Link href="/analysis" className="text-gray-700 hover:text-indigo-600 font-medium transition-colors">
              Skills
            </Link>
            <Link href="/courses" className="text-gray-700 hover:text-indigo-600 font-medium transition-colors">
              Jobs
            </Link>
            <Link href="/learning" className="text-gray-700 hover:text-indigo-600 font-medium transition-colors">
              Learning
            </Link>
          </div>

          {/* Auth Buttons */}
          <div className="hidden md:flex items-center space-x-4">
            <Link 
              href="/auth" 
              className="text-gray-700 hover:text-indigo-600 font-medium transition-colors"
            >
              Login
            </Link>
            <Link 
              href="/auth" 
              className="bg-indigo-600 text-white px-4 py-2 rounded-lg font-medium hover:bg-indigo-700 transition-colors"
            >
              Sign Up
            </Link>
          </div>

          {/* Mobile menu button */}
          <div className="md:hidden">
            <button
              onClick={() => setIsMenuOpen(!isMenuOpen)}
              className="text-gray-700 hover:text-indigo-600 transition-colors"
            >
              {isMenuOpen ? <X size={24} /> : <Menu size={24} />}
            </button>
          </div>
        </div>

        {/* Mobile menu */}
        {isMenuOpen && (
          <div className="md:hidden">
            <div className="px-2 pt-2 pb-3 space-y-1 bg-white border-t border-gray-200">
              <Link href="/" className="block px-3 py-2 text-gray-700 hover:text-indigo-600 font-medium">
                Home
              </Link>
              <Link href="/dashboard" className="block px-3 py-2 text-gray-700 hover:text-indigo-600 font-medium">
                Resume
              </Link>
              <Link href="/analysis" className="block px-3 py-2 text-gray-700 hover:text-indigo-600 font-medium">
                Skills
              </Link>
              <Link href="/courses" className="block px-3 py-2 text-gray-700 hover:text-indigo-600 font-medium">
                Jobs
              </Link>
              <Link href="/learning" className="block px-3 py-2 text-gray-700 hover:text-indigo-600 font-medium">
                Learning
              </Link>
              <div className="border-t border-gray-200 pt-3 mt-3">
                <Link href="/auth" className="block px-3 py-2 text-gray-700 hover:text-indigo-600 font-medium">
                  Login
                </Link>
                <Link href="/auth" className="block px-3 py-2 bg-indigo-600 text-white rounded-lg font-medium mx-3 text-center">
                  Sign Up
                </Link>
              </div>
            </div>
          </div>
        )}
      </div>
    </nav>
  );
}