"use client";

import Navbar from "@/components/landing/Navbar";
import HeroSection from "@/components/landing/HeroSection";
import CompanyLogos from "@/components/landing/CompanyLogos";
import FeatureCards from "@/components/landing/FeatureCards";
import HowItWorks from "@/components/landing/HowItWorks";
import CareerInsights from "@/components/landing/CareerInsights";
import ResumePreview from "@/components/landing/ResumePreview";
import JobMatching from "@/components/landing/JobMatching";
import SkilloraAI from "@/components/landing/SkilloraAI";
import FinalCTA from "@/components/landing/FinalCTA";
import Footer from "@/components/landing/Footer";

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-white">
      <Navbar />
      <HeroSection />
      <CompanyLogos />
      <FeatureCards />
      <HowItWorks />
      <CareerInsights />
      <ResumePreview />
      <JobMatching />
      <SkilloraAI />
      <FinalCTA />
      <Footer />
    </div>
  );
}