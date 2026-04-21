"""
MOLIT 실거래가 OpenAPI 클라이언트

국토교통부 아파트 매매 실거래가 OpenAPI를 호출하여
정규화된 DataFrame으로 반환한다.

API Docs: https://www.data.go.kr/data/15057511/openapi.do
Endpoint: getRTMSDataSvcAptTrade
"""
from __future__ import annotations

import os
import logging
from typing import Iterable, Optional
from dataclasses import dataclass

import pandas as pd
import requests
from tqdm import tqdm
from dotenv import load_dotenv

logger = logging.getLogger(__name__)
load_dotenv()


@dataclass
class MolitQueryParams:
    """MOLIT API 요청 파라미터."""
    region_code: str          # 법정동 5자리 (예: '11680' = 강남구)
    year_month: str           # 'YYYYMM' (예: '202601')
    page_no: int = 1
    num_of_rows: int = 1000


class MolitClient:
    """
    국토교통부 아파트 매매 실거래가 API 클라이언트.

    Attributes:
        api_key: 공공데이터포털 인증키 (환경변수 MOLIT_API_KEY 자동 로드)
        base_url: API 베이스 URL
        timeout: 요청 타임아웃 (초)

    Example:
        >>> client = MolitClient()
        >>> df = client.fetch_transactions("11680", "202601")
        >>> df.shape
        (347, 24)
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: int = 30,
    ):
        self.api_key = api_key or os.getenv("MOLIT_API_KEY")
        if not self.api_key:
            raise ValueError(
                "MOLIT_API_KEY가 설정되지 않았습니다. "
                ".env 파일 또는 환경변수를 확인하세요."
            )
        self.base_url = base_url or os.getenv(
            "MOLIT_API_BASE",
            "http://openapi.molit.go.kr/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc"
        )
        self.timeout = timeout
        self.endpoint = f"{self.base_url}/getRTMSDataSvcAptTrade"

    # ------------------------------------------------------------------
    # Public Methods
    # ------------------------------------------------------------------
    def fetch_transactions(
        self,
        region_code: str,
        year_month: str,
        all_pages: bool = True,
    ) -> pd.DataFrame:
        """
        단일 지역·단월 실거래 데이터 조회.

        Args:
            region_code: 법정동 코드 5자리 (예: '11680')
            year_month: 조회 년월 'YYYYMM' (예: '202601')
            all_pages: True면 모든 페이지를 순회하여 병합

        Returns:
            정규화된 실거래 DataFrame. 주요 컬럼:
                - deal_amount (int): 거래금액 (만원)
                - deal_year, deal_month, deal_day (int)
                - area (float): 전용면적 (㎡)
                - apt_name (str): 단지명
                - jibun (str): 지번
                - legal_dong (str): 법정동명
                - floor (int): 층
                - build_year (int): 건축연도

        Raises:
            requests.HTTPError: API 호출 실패 시
            ValueError: region_code·year_month 형식 오류 시
        """
        raise NotImplementedError(
            "TODO: _call_single_page()를 all_pages 루프로 호출하고 "
            "_normalize_columns()로 컬럼명 통일"
        )

    def fetch_multi_period(
        self,
        region_codes: Iterable[str],
        year_months: Iterable[str],
    ) -> pd.DataFrame:
        """
        다지역·다월 데이터 병렬 조회 후 pandas.concat으로 병합.

        Returns:
            모든 구·월 조합의 통합 DataFrame.
            tqdm 프로그레스바로 진행 상태 표시.
        """
        raise NotImplementedError("TODO: itertools.product로 조합 생성 후 순회")

    # ------------------------------------------------------------------
    # Private Helpers
    # ------------------------------------------------------------------
    def _call_single_page(self, params: MolitQueryParams) -> pd.DataFrame:
        """단일 페이지 API 호출. XML 파싱 후 DataFrame 반환."""
        raise NotImplementedError(
            "TODO: requests.get() + xml.etree.ElementTree 파싱"
        )

    def _normalize_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """MOLIT 한글 컬럼명을 영문 snake_case로 변환, 타입 캐스팅."""
        raise NotImplementedError(
            "TODO: COLUMN_MAP dict 정의 후 df.rename(), "
            "거래금액 쉼표 제거·int 변환"
        )

    @staticmethod
    def _validate_region_code(code: str) -> None:
        """region_code가 5자리 숫자인지 검증."""
        if not (isinstance(code, str) and len(code) == 5 and code.isdigit()):
            raise ValueError(f"region_code는 5자리 숫자 문자열이어야 합니다: {code}")

    @staticmethod
    def _validate_year_month(ym: str) -> None:
        """year_month가 'YYYYMM' 형식인지 검증."""
        if not (isinstance(ym, str) and len(ym) == 6 and ym.isdigit()):
            raise ValueError(f"year_month는 'YYYYMM' 형식이어야 합니다: {ym}")


# ----------------------------------------------------------------------
# MOLIT → 내부 컬럼 매핑 (참조용)
# ----------------------------------------------------------------------
COLUMN_MAP = {
    "거래금액": "deal_amount",
    "거래유형": "deal_type",
    "건축년도": "build_year",
    "년": "deal_year",
    "월": "deal_month",
    "일": "deal_day",
    "법정동": "legal_dong",
    "아파트": "apt_name",
    "전용면적": "area",
    "지번": "jibun",
    "지역코드": "region_code",
    "층": "floor",
    "해제사유발생일": "cancel_date",
    "해제여부": "cancel_flag",
}
