from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.session import get_session
from app.logging.logger import logger
from app.schemas.userschema import (
    UserCreateRequest,
    UserLoginRequest,
    UserLoginResponse,
    UserResponse,
)
from app.services.auth_service import (
    login_user,
    register_user,
)
router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)
@router.post(
    "/register",
    response_model=UserResponse
)
async def register(
    user_data: UserCreateRequest,
    session: AsyncSession = Depends(get_session)
):
    logger.info(
        "Registration attempt for username={}",
        user_data.username
    )
    try:
        user = await register_user(
            session=session,
            user_data=user_data
        )
        logger.info(
            "Registration successful for username={}",
            user.username
        )
        return user
    except ValueError as error:
        logger.warning(
            "Registration failed for username={}: {}",
            user_data.username,
            error
        )
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )
    except Exception as error:
        logger.error(
            "Unexpected error during registration for username={}: {}",
            user_data.username,
            error
        )
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )
@router.post(
    "/login",
    response_model=UserLoginResponse
)
async def login(
    user_data: UserLoginRequest,
    session: AsyncSession = Depends(get_session)
):

    logger.info(
        "Login attempt for username={}",
        user_data.username
    )

    try:

        user, access_token = await login_user(
            session=session,
            username=user_data.username,
            password=user_data.password
        )

        logger.info(
            "Login successful for username={}",
            user.username
        )

        return UserLoginResponse(
            message="Login successful",
            access_token=access_token,
            token_type="bearer",
            user=user
        )
    except ValueError as error:
        logger.warning(
            "Login failed for username={}: {}",
            user_data.username,
            error
        )
        raise HTTPException(
            status_code=401,
            detail=str(error)
        )
    except Exception as error:
        logger.error(
            "Unexpected error during login for username={}: {}",
            user_data.username,
            error
        )
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )