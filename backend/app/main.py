"""
FIXXY — Car Spare Parts & Billing Management System
FastAPI Main Application
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.core.config import settings
from app.database import db

# Import API routers
from app.api import auth, products, orders, coupons, vehicles, settings as settings_api

# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    description="Car Spare Parts & Billing Management System - Drive Better • Fix Smarter",
    version=settings.APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(auth.router)
app.include_router(products.router)
app.include_router(orders.router)
app.include_router(coupons.router)
app.include_router(vehicles.router)
app.include_router(settings_api.router)


# Root endpoint
@app.get("/")
async def root():
    """
    Root endpoint - API information
    """
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "tagline": "Drive Better • Fix Smarter",
        "description": "Car Spare Parts & Billing Management System API",
        "docs": "/docs",
        "status": "running"
    }


# Health check endpoint
@app.get("/health")
async def health_check():
    """
    Health check endpoint
    Tests database connectivity
    """
    try:
        db_ok = db.test_connection()
        
        if db_ok:
            return {
                "status": "healthy",
                "database": "connected",
                "version": settings.APP_VERSION
            }
        else:
            return JSONResponse(
                status_code=503,
                content={
                    "status": "unhealthy",
                    "database": "disconnected",
                    "version": settings.APP_VERSION
                }
            )
    except Exception as e:
        return JSONResponse(
            status_code=503,
            content={
                "status": "error",
                "message": str(e),
                "version": settings.APP_VERSION
            }
        )


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """
    Global exception handler for unhandled errors
    """
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            "message": str(exc) if settings.DEBUG else "An error occurred"
        }
    )


# Startup event
@app.on_event("startup")
async def startup_event():
    """
    Run on application startup
    """
    print("=" * 70)
    print(f"🚗 {settings.APP_NAME} API Starting...")
    print(f"Version: {settings.APP_VERSION}")
    print(f"Environment: {'Development' if settings.DEBUG else 'Production'}")
    print(f"Database: {settings.MYSQL_DATABASE} @ {settings.MYSQL_HOST}:{settings.MYSQL_PORT}")
    print("=" * 70)
    
    # Test database connection
    try:
        if db.test_connection():
            print("✅ Database connection successful")
        else:
            print("❌ Database connection failed")
    except Exception as e:
        print(f"❌ Database error: {e}")
    
    print("=" * 70)
    print(f"📚 API Documentation: http://localhost:8000/docs")
    print(f"🔄 ReDoc Documentation: http://localhost:8000/redoc")
    print("=" * 70)


# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """
    Run on application shutdown
    """
    print("=" * 70)
    print(f"🚗 {settings.APP_NAME} API Shutting down...")
    print("=" * 70)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8000,
        reload=settings.DEBUG
    )
