# Frontend

React + Vite frontend for Shopify Store Health Scanner.

## Setup

```bash
# Install dependencies
npm install

# Start dev server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

Dev server runs on: http://localhost:5173

## Configuration

Update API URL in `src/App.jsx`:

```javascript
// Local development
const API_URL = 'http://localhost:8000';

// Production
const API_URL = 'https://yourapp.railway.app';
```

## Tech Stack

- **React 18** - UI library
- **Vite** - Build tool
- **Tailwind CSS** - Styling
- **Lucide React** - Icons

## Project Structure

```
src/
├── App.jsx       # Main component
├── main.jsx      # Entry point
└── index.css     # Tailwind imports
```

## Deploy to Netlify

### Option 1: CLI
```bash
npm run build
npm install -g netlify-cli
netlify deploy --prod
```

### Option 2: Drag & Drop
1. Run `npm run build`
2. Go to https://app.netlify.com/drop
3. Drag the `dist` folder

### Option 3: GitHub
1. Push code to GitHub
2. Connect repo to Netlify
3. Build command: `npm run build`
4. Publish directory: `dist`

## Environment Variables

No environment variables needed. Update `API_URL` directly in `App.jsx`.

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

## Tailwind Configuration

See `tailwind.config.js` for customization options.

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)