/**
 * Search Bar Component
 * 
 * Executive function optimized search with:
 * - Debounced input to reduce cognitive load
 * - Clear visual feedback for ADHD support  
 * - Predictable behavior for autism support
 * - Accessible keyboard navigation
 */

'use client';

import { Filter, Search, X } from 'lucide-react';
import React, { useEffect, useRef, useState } from 'react';

interface SearchBarProps {
  value: string;
  onChange: (value: string) => void;
  placeholder?: string;
  executiveFunctionEnabled: boolean;
  onFilterClick?: () => void;
  className?: string;
}

export const SearchBar: React.FC<SearchBarProps> = ({
  value,
  onChange,
  placeholder = "Search tools and domains...",
  executiveFunctionEnabled,
  onFilterClick,
  className = ''
}) => {
  const [localValue, setLocalValue] = useState(value);
  const [isFocused, setIsFocused] = useState(false);
  const inputRef = useRef<HTMLInputElement>(null);
  const debounceRef = useRef<NodeJS.Timeout>();

  // Debounced search for executive function support
  useEffect(() => {
    if (debounceRef.current) {
      clearTimeout(debounceRef.current);
    }

    debounceRef.current = setTimeout(() => {
      onChange(localValue);
    }, executiveFunctionEnabled ? 200 : 300);

    return () => {
      if (debounceRef.current) {
        clearTimeout(debounceRef.current);
      }
    };
  }, [localValue, onChange, executiveFunctionEnabled]);

  // Sync with external value changes
  useEffect(() => {
    setLocalValue(value);
  }, [value]);

  const handleClear = () => {
    setLocalValue('');
    if (inputRef.current) {
      inputRef.current.focus();
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Escape') {
      handleClear();
    }
  };

  return (
    <div className={`search-bar-container ${className}`}>
      <div 
        className={`
          relative 
          flex 
          items-center 
          bg-white 
          border-2 
          rounded-lg 
          transition-all 
          duration-200
          ${isFocused 
            ? 'border-blue-500 ring-2 ring-blue-500 ring-opacity-20' 
            : 'border-gray-300 hover:border-gray-400'
          }
          ${executiveFunctionEnabled ? 'transform-gpu' : ''}
        `}
      >
        {/* Search Icon */}
        <div className="flex items-center justify-center w-12 h-12">
          <Search 
            className={`w-5 h-5 transition-colors duration-200 ${
              isFocused ? 'text-blue-500' : 'text-gray-400'
            }`} 
          />
        </div>

        {/* Input Field */}
        <input
          ref={inputRef}
          type="text"
          value={localValue}
          onChange={(e) => setLocalValue(e.target.value)}
          onFocus={() => setIsFocused(true)}
          onBlur={() => setIsFocused(false)}
          onKeyDown={handleKeyDown}
          placeholder={placeholder}
          className="
            flex-1 
            h-12 
            bg-transparent 
            border-none 
            outline-none 
            text-gray-900 
            placeholder-gray-500
            text-base
          "
          aria-label="Search tools and domains"
        />

        {/* Clear Button */}
        {localValue && (
          <button
            onClick={handleClear}
            className="
              flex 
              items-center 
              justify-center 
              w-8 
              h-8 
              mx-2 
              text-gray-400 
              hover:text-gray-600 
              rounded-full 
              hover:bg-gray-100 
              transition-colors 
              duration-150
            "
            aria-label="Clear search"
          >
            <X className="w-4 h-4" />
          </button>
        )}

        {/* Filter Button */}
        {onFilterClick && (
          <button
            onClick={onFilterClick}
            className="
              flex 
              items-center 
              justify-center 
              w-12 
              h-12 
              text-gray-400 
              hover:text-gray-600 
              border-l 
              border-gray-200 
              hover:bg-gray-50 
              transition-colors 
              duration-150
            "
            aria-label="Open search filters"
          >
            <Filter className="w-5 h-5" />
          </button>
        )}
      </div>

      {/* Executive Function Indicator */}
      {executiveFunctionEnabled && isFocused && (
        <div className="mt-2 text-xs text-gray-500 flex items-center space-x-1">
          <div className="w-2 h-2 bg-green-400 rounded-full"></div>
          <span>Executive function optimized - reduced search delay</span>
        </div>
      )}

      {/* Search Tips */}
      {isFocused && !localValue && (
        <div className="absolute top-full left-0 right-0 mt-2 p-3 bg-white border border-gray-200 rounded-lg shadow-lg z-10">
          <div className="text-sm text-gray-600 space-y-1">
            <p className="font-medium">Quick search tips:</p>
            <ul className="text-xs space-y-1 ml-2">
              <li>• Type tool names: "MISP", "n8n", "Commander Spellbook"</li>
              <li>• Search by domain: "security", "productivity", "mtg"</li>
              <li>• Find by feature: "forensics", "automation", "analysis"</li>
              <li>• Press Escape to clear</li>
            </ul>
          </div>
        </div>
      )}
    </div>
  );
};