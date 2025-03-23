import React, { useState } from 'react';
import { NewLink, API_BASE_URL } from '../types';

interface UTMGeneratorProps {
  baseUrl: string;
}

const UTMGenerator: React.FC<UTMGeneratorProps> = ({ baseUrl }) => {
  const [formData, setFormData] = useState<NewLink>({
    title: '',
    destination_url: '',
    slug: '',
  });

  const [generatedLink, setGeneratedLink] = useState<string>('');
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<boolean>(false);

  // Generate a slug from the title
  const generateSlug = (title: string): string => {
    return title
      .toLowerCase()
      .replace(/[^\w\s-]/g, '')
      .replace(/[\s_-]+/g, '-')
      .replace(/^-+|-+$/g, '');
  };

  // Handle input changes
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));

    // Auto-generate slug when title changes
    if (name === 'title') {
      setFormData((prev) => ({
        ...prev,
        slug: generateSlug(value),
      }));
    }
  };

  // Handle form submission
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError(null);
    setSuccess(false);

    try {
      const response = await fetch(`${API_BASE_URL}/links/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to create link');
      }

      const data = await response.json();
      
      // Generate the tracking URL
      const trackingUrl = `${baseUrl}/go/${data.slug}`;
      setGeneratedLink(trackingUrl);
      setSuccess(true);
      
      // Reset form
      setFormData({
        title: '',
        destination_url: '',
        slug: '',
      });
    } catch (err) {
      if (err instanceof Error) {
        setError(err.message);
      } else {
        setError('An unknown error occurred');
      }
    } finally {
      setIsLoading(false);
    }
  };

  // Handle copy to clipboard
  const copyToClipboard = () => {
    navigator.clipboard.writeText(generatedLink);
    alert('Link copied to clipboard!');
  };

  return (
    <div className="bg-white shadow rounded-lg p-6 mb-8">
      <h2 className="text-2xl font-bold text-gray-900 mb-4">UTM Link Generator</h2>
      <p className="text-gray-600 mb-6">
        Create trackable links for your YouTube videos. These links will redirect to your destination URL
        with UTM parameters automatically added.
      </p>

      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label htmlFor="title" className="block text-sm font-medium text-gray-700">
            Video Title
          </label>
          <input
            type="text"
            name="title"
            id="title"
            value={formData.title}
            onChange={handleChange}
            required
            className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
            placeholder="How to Close More Clients"
          />
        </div>

        <div>
          <label htmlFor="slug" className="block text-sm font-medium text-gray-700">
            Slug (Auto-generated)
          </label>
          <input
            type="text"
            name="slug"
            id="slug"
            value={formData.slug}
            onChange={handleChange}
            className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
            placeholder="how-to-close-more-clients"
          />
          <p className="mt-1 text-xs text-gray-500">
            This will be used in your tracking URL: {baseUrl}/go/<span className="font-mono">{formData.slug || 'your-slug'}</span>
          </p>
        </div>

        <div>
          <label htmlFor="destination_url" className="block text-sm font-medium text-gray-700">
            Destination URL
          </label>
          <input
            type="url"
            name="destination_url"
            id="destination_url"
            value={formData.destination_url}
            onChange={handleChange}
            required
            className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
            placeholder="https://calendly.com/your-name/15min"
          />
          <p className="mt-1 text-xs text-gray-500">
            The URL where users will be redirected (e.g., your Calendly link)
          </p>
        </div>

        <div>
          <button
            type="submit"
            disabled={isLoading}
            className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
          >
            {isLoading ? 'Generating...' : 'Generate Tracking Link'}
          </button>
        </div>
      </form>

      {error && (
        <div className="mt-4 bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-md">
          <p>{error}</p>
        </div>
      )}

      {success && generatedLink && (
        <div className="mt-6 bg-green-50 border border-green-200 p-4 rounded-md">
          <h3 className="text-lg font-medium text-green-800 mb-2">Link Generated!</h3>
          <div className="bg-white border border-gray-300 rounded p-3 flex items-center justify-between">
            <code className="text-sm break-all">{generatedLink}</code>
            <button
              onClick={copyToClipboard}
              className="ml-2 inline-flex items-center px-3 py-1 border border-transparent text-sm leading-4 font-medium rounded-md text-indigo-700 bg-indigo-100 hover:bg-indigo-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
            >
              Copy
            </button>
          </div>
          <p className="mt-2 text-sm text-green-700">
            This link will redirect to your destination URL with proper UTM parameters.
          </p>
        </div>
      )}
    </div>
  );
};

export default UTMGenerator; 