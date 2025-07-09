# LMAO_DED - Video Creation Web Application

A Flask-based web application that allows users to create videos from image sequences with custom transitions, durations, and background music.

## Features

### User Management
- **User Registration & Login**: Secure user authentication system
- **Session Management**: Persistent user sessions
- **Admin Dashboard**: Administrative interface for user and image management
- **Individual User Workspaces**: Isolated file storage per user

### Video Creation
- **Image Upload**: Support for PNG, JPG, JPEG, and GIF formats
- **Custom Durations**: Set individual display time for each image
- **Multiple Transitions**: 
  - None (direct cut)
  - Cross Fade
  - Slide In (Left, Right, Top, Bottom)
- **Background Music**: Add audio tracks to videos
- **Video Export**: Download created videos as MP4 files

### Image Management
- **Bulk Upload**: Upload multiple images simultaneously
- **Image Preview**: View uploaded images in the workspace
- **Delete Images**: Remove unwanted images from projects
- **Automatic Resizing**: Images resized to 1600x900 resolution

## Technology Stack

- **Backend**: Flask (Python)
- **Database**: CockroachDB (PostgreSQL compatible)
- **Video Processing**: MoviePy
- **Image Processing**: PIL (Pillow)
- **Frontend**: HTML templates with Jinja2

## Setup

### Prerequisites
- Python 3.7+
- CockroachDB account (or PostgreSQL)
- Required Python packages (see installation)

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd lmao_ded
```

2. Install dependencies:
```bash
pip install flask moviepy pillow psycopg2-binary imageio
```

3. Database Setup:
   - Create a CockroachDB cluster or PostgreSQL database
   - Update database connection parameters in `app.py`
   - Ensure you have the SSL certificate (`root.crt`) if using CockroachDB

4. Create required database tables:
```sql
CREATE TABLE user_info (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(100) NOT NULL
);

CREATE TABLE image_data (
    image_id SERIAL PRIMARY KEY,
    image_path VARCHAR(255) NOT NULL,
    user_id INTEGER REFERENCES user_info(id),
    image_size INTEGER,
    image_name VARCHAR(255),
    image_extension VARCHAR(10)
);
```

5. Create required directories:
```bash
mkdir -p static/uploads
mkdir -p templates
```

6. Run the application:
```bash
python app.py
```

The application will be available at `http://localhost:5000`

## Project Structure

```
├── app.py              # Main Flask application
├── maker.py            # Video creation logic
├── transitions.py      # Video transition effects
├── static/
│   ├── uploads/        # User uploaded images and generated videos
│   └── audio/          # Background music files
├── templates/          # HTML templates
├── root.crt           # SSL certificate for CockroachDB
└── README.md
```

## Usage

### For Users

1. **Register/Login**: Create an account or log in to existing account
2. **Upload Images**: Use the file upload interface to add images
3. **Set Parameters**: Configure duration for each image and select transitions
4. **Add Music**: Choose background audio (optional)
5. **Create Video**: Generate the video with your specifications
6. **Download**: Save the created video to your device

### For Administrators

- Access admin panel at `/admin` with credentials: `admin@admin` / `admin`
- View user statistics and manage accounts
- Monitor image uploads and system usage

## API Endpoints

- `GET /` - Home page
- `GET|POST /login` - User authentication
- `GET|POST /register` - User registration
- `GET /workarea` - User workspace
- `POST /upload` - Image upload
- `POST /deleteimage` - Remove images
- `POST|GET /createVideo` - Video generation
- `GET /downloadVideo` - Video download
- `GET /admin` - Admin dashboard
- `GET /logout` - User logout

## Video Transitions

The application supports several transition types:

1. **None (0)**: Direct cut between images
2. **Cross Fade (1)**: Smooth fade transition
3. **Slide In Left (2)**: New image slides from left
4. **Slide In Right (3)**: New image slides from right  
5. **Slide In Top (4)**: New image slides from top
6. **Slide In Bottom (5)**: New image slides from bottom

## Configuration

### Database Connection
Update the connection parameters in `app.py`:
```python
conn_params = {
    'host': 'your-database-host',
    'port': 26257,
    'user': 'your-username',
    'password': 'your-password',
    'database': 'your-database-name',
    'sslmode': 'verify-full',
    'sslrootcert': 'root.crt'
}
```

### Video Settings
Modify video output settings in `maker.py`:
```python
HEIGHT, WIDTH = 900, 1600  # Video resolution
fps = 10                   # Frames per second
```

## Known Issues

- IIIT network compatibility issues with CockroachDB
- Large image files may cause processing delays
- Video generation time depends on number of images and transitions

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For issues or questions:
1. Check existing issues in the repository
2. Create a new issue with detailed description
3. Include error logs and system information
