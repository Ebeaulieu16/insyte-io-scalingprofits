# Insyte.io - YouTube + Sales Dashboard

A powerful dashboard that helps online businesses track YouTube video performance and sales funnel metrics.

## Features

- Track performance from YouTube video views to closed deals
- Generate UTM tracking links for YouTube videos
- Monitor sales funnel conversions with detailed metrics
- Visualize data with interactive charts
- Attribute revenue back to specific videos

## Tech Stack

- **Frontend**: React with TypeScript and TailwindCSS
- **Backend**: FastAPI with SQLite database
- **Charts**: Chart.js with React-ChartJS-2

## Quick Start

### Backend Setup

1. Navigate to the backend directory:
   ```
   cd backend
   ```

2. Activate the virtual environment:
   ```
   source venv/bin/activate  # On Unix/macOS
   # OR
   .\venv\Scripts\activate  # On Windows
   ```

3. Set up your API keys in the `.env` file:
   ```
   # Copy the example .env file
   cp .env.example .env
   
   # Edit the .env file with your API keys
   nano .env  # or use any text editor
   ```

4. Run the FastAPI server:
   ```
   python run.py
   ```

5. The API will be available at http://localhost:8001
   - API Documentation: http://localhost:8001/docs
   - API Status: http://localhost:8001/status/health

### Frontend Setup

1. Navigate to the frontend directory:
   ```
   cd frontend
   ```

2. Install dependencies:
   ```
   npm install
   ```

3. Start the development server:
   ```
   npm run dev
   ```

4. The frontend will be available at http://localhost:5173

## Production Deployment

### Prerequisites

- A server with Python 3.9+ and Node.js 18+
- Domain name pointing to your server
- (Optional) A PostgreSQL database for production use

### Backend Deployment

1. Clone the repository on your server:
   ```bash
   git clone https://github.com/yourusername/insyte-io.git
   cd insyte-io/backend
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up your environment variables:
   ```bash
   cp .env.example .env
   # Edit the .env file with your production settings
   nano .env
   ```

5. Important environment settings for production:
   - Set `ENVIRONMENT="production"`
   - Generate a secure `SECRET_KEY`
   - Add all your API keys
   - (Optional) Configure a PostgreSQL database URL

6. Run the backend with a production server like Uvicorn behind Nginx:
   ```bash
   # Install uvicorn
   pip install uvicorn[standard]
   
   # Run with multiple workers
   uvicorn app.main:app --host 0.0.0.0 --port 8001 --workers 4
   ```

7. For proper production deployment, use a service manager like systemd to keep the server running.

### Frontend Deployment

1. Navigate to the frontend directory:
   ```bash
   cd insyte-io/frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Create a `.env.production` file:
   ```
   VITE_API_URL=https://api.yourdomain.com
   ```

4. Build for production:
   ```bash
   npm run build:prod
   ```

5. The build output will be in the `dist` directory. Serve these files with Nginx or another web server.

### Nginx Configuration Example

```nginx
# Frontend
server {
    listen 80;
    server_name yourdomain.com;
    
    location / {
        root /path/to/insyte-io/frontend/dist;
        try_files $uri $uri/ /index.html;
    }
    
    # Proxy API requests to the backend
    location /api/ {
        proxy_pass http://localhost:8001/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}

# API Subdomain (optional)
server {
    listen 80;
    server_name api.yourdomain.com;
    
    location / {
        proxy_pass http://localhost:8001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

For a complete production setup, you should also:
- Set up HTTPS with Let's Encrypt
- Configure proper logging
- Set up database backups
- Implement a CI/CD pipeline for automated deployment

## API Integrations

### YouTube API

The YouTube API is used to fetch video statistics like views, likes, and comments.

1. Get a YouTube API key from the [Google Cloud Console](https://console.cloud.google.com/)
2. Enable the YouTube Data API v3
3. Add your API key to the `.env` file:
   ```
   YOUTUBE_API_KEY="your_youtube_api_key_here"
   ```

### Calendly API

Calendly integration allows tracking bookings made through Calendly.

1. Get a Calendly API key from your [Calendly integrations page](https://calendly.com/integrations)
2. Set up webhooks in Calendly to point to `https://your-domain.com/webhooks/calendly`
3. Add your API key to the `.env` file:
   ```
   CALENDLY_API_KEY="your_calendly_api_key_here"
   CALENDLY_WEBHOOK_SECRET="your_calendly_webhook_secret_here"
   ```

### Cal.com API

Cal.com integration allows tracking bookings made through Cal.com.

1. Get a Cal.com API key from your Cal.com settings
2. Set up webhooks in Cal.com to point to `https://your-domain.com/webhooks/calcom`
3. Add your API key to the `.env` file:
   ```
   CALCOM_API_KEY="your_calcom_api_key_here"
   ```

### Stripe API

Stripe integration allows tracking sales and revenue.

1. Get a Stripe API key from your [Stripe Dashboard](https://dashboard.stripe.com/apikeys)
2. Set up webhooks in Stripe to point to `https://your-domain.com/webhooks/stripe`
3. Add your API keys to the `.env` file:
   ```
   STRIPE_API_KEY="your_stripe_api_key_here"
   STRIPE_WEBHOOK_SECRET="your_stripe_webhook_secret_here"
   ```

## UTM Tracking Flow

Insyte.io provides end-to-end tracking from YouTube video views to sales through UTM parameters:

1. **Generate a tracking link**: Create a tracking link for your YouTube video using the UTM Generator
2. **Share the link**: Add the link to your YouTube video description
3. **Track clicks**: When users click the link, Insyte.io logs the click and redirects to your booking page with UTM parameters
4. **Track bookings**: Calendly/Cal.com webhooks capture the booking with the UTM parameters
5. **Track sales**: Stripe webhooks capture the sale and link it back to the original booking and click
6. **View attribution**: See the complete customer journey in the dashboard from video view to sale

### Example UTM Flow

```
YouTube Video -> Tracking Link -> Cal.com/Calendly Booking -> Stripe Payment
```

Each step in this flow is tracked and connected, allowing you to see which videos generate the most revenue.

## How to Use

1. **Generate Demo Data**: Click the "Load Demo Data" button to populate the dashboard with sample data.

2. **Create Tracking Links**: Use the UTM Generator at the bottom of the page to create tracking links for your YouTube videos.

3. **Share Links**: Share the generated tracking links in your YouTube video descriptions.

4. **Monitor Performance**: Watch the dashboard as clicks, bookings, and sales come in.

## Troubleshooting

If you encounter issues with API integrations:

1. Check the API Status section on the dashboard
2. Verify that your API keys are correctly configured in the `.env` file
3. Check the server logs for specific error messages
4. Ensure webhooks are properly configured on the respective platforms

## Project Structure

```
insyte-io/
├── backend/          # FastAPI backend
│   ├── app/
│   │   ├── models/   # Database models
│   │   ├── routes/   # API endpoints
│   │   ├── schemas/  # Pydantic schemas
│   │   ├── services/ # API integrations
│   │   └── main.py   # Main application entry
│   └── venv/         # Python virtual environment
│
└── frontend/         # React frontend
    ├── public/       # Static files
    ├── src/
    │   ├── components/ # React components
    │   ├── types.ts    # TypeScript interfaces
    │   └── App.tsx     # Main application component
    └── index.html    # HTML entry point
```

## License

MIT 