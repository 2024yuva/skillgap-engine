"use client";

const companies = [
  { name: "FedEx", color: "bg-purple-100 text-purple-600" },
  { name: "Orange", color: "bg-orange-100 text-orange-600" }, 
  { name: "Microsoft", color: "bg-blue-100 text-blue-600" },
  { name: "Amazon", color: "bg-yellow-100 text-yellow-600" },
  { name: "Walmart", color: "bg-cyan-100 text-cyan-600" },
  { name: "AT&T", color: "bg-gray-100 text-gray-600" }
];

export default function CompanyLogos() {
  return (
    <section className="py-16 bg-indigo-600">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-12">
          <h2 className="text-3xl font-bold text-white mb-4">
            Customers have been hired by:
          </h2>
          <p className="text-indigo-200 text-lg">
            Our AI-powered career guidance has helped professionals land jobs at top companies
          </p>
        </div>

        {/* Spinning Logos Container */}
        <div className="relative">
          {/* First Row - Left to Right */}
          <div className="flex overflow-hidden mb-8">
            <div className="flex animate-scroll-left space-x-12">
              {[...companies, ...companies].map((company, index) => (
                <div 
                  key={`${company.name}-${index}`}
                  className="flex-shrink-0 w-32 h-20 bg-white/10 backdrop-blur-sm rounded-xl flex items-center justify-center border border-white/20 hover:bg-white/20 transition-all duration-300"
                >
                  <div className="text-white font-bold text-lg">
                    {company.name}
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Second Row - Right to Left */}
          <div className="flex overflow-hidden">
            <div className="flex animate-scroll-right space-x-12">
              {[...companies.slice().reverse(), ...companies.slice().reverse()].map((company, index) => (
                <div 
                  key={`${company.name}-reverse-${index}`}
                  className="flex-shrink-0 w-32 h-20 bg-white/10 backdrop-blur-sm rounded-xl flex items-center justify-center border border-white/20 hover:bg-white/20 transition-all duration-300"
                >
                  <div className="text-white font-bold text-lg">
                    {company.name}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-8 mt-16 pt-16 border-t border-white/20">
          <div className="text-center">
            <div className="text-3xl font-bold text-white mb-2">95%</div>
            <div className="text-indigo-200">Success Rate</div>
          </div>
          <div className="text-center">
            <div className="text-3xl font-bold text-white mb-2">10K+</div>
            <div className="text-indigo-200">Careers Built</div>
          </div>
          <div className="text-center">
            <div className="text-3xl font-bold text-white mb-2">500+</div>
            <div className="text-indigo-200">Companies</div>
          </div>
          <div className="text-center">
            <div className="text-3xl font-bold text-white mb-2">24/7</div>
            <div className="text-indigo-200">AI Support</div>
          </div>
        </div>
      </div>

      <style jsx>{`
        @keyframes scroll-left {
          0% { transform: translateX(0); }
          100% { transform: translateX(-50%); }
        }
        
        @keyframes scroll-right {
          0% { transform: translateX(-50%); }
          100% { transform: translateX(0); }
        }
        
        .animate-scroll-left {
          animation: scroll-left 30s linear infinite;
        }
        
        .animate-scroll-right {
          animation: scroll-right 30s linear infinite;
        }
      `}</style>
    </section>
  );
}