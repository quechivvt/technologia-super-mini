from fastapi import APIRouter,Depends, status
from app.schemas.openai_schema import OpenAIRequest, OpenAIResponse
from app.core.dependencies import get_openai_service
from app.service.openai_service import OpenAIService


router = APIRouter(
    prefix="/chat",
    tags=["Open AI"],
)

@router.post(
    "/",
    response_model=OpenAIResponse,
    status_code=status.HTTP_200_OK)
async def chat(
    request: OpenAIRequest,
    openai_service: OpenAIService = Depends(get_openai_service)
): 
    #response = await client.responses.create(
    #    model=settings.GEMINI_MODEL,
    #    input=request.message,
    #)

    #return OpenAIResponse(response, datetime.now(t_hcm = datetime.now(ZoneInfo("Asia/Ho_Chi_Minh"))))
    return await openai_service.chat(message = request.message)
    
    
    
