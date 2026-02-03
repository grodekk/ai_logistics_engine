@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "ok", "service": "AI Logistics Engine"}


@app.get("/routes/available", tags=["Routes"])
async def get_available_routes():
    df = dp.get_routes_costs()
    routes = df['route_name'].unique().tolist()
    return {"routes": routes}


@app.post("/decision/rates", response_model=RatesResponse, tags=["Decision Engine"])
async def calculate_route_rates(
        routes: List[RouteInput],
        monthly_profit_target: float
):
    result = decision_engine.calculate_rates_for_routes(
        routes_info=[r.model_dump() for r in routes],
        monthly_profit_target=monthly_profit_target
    )

    df = result["df"]

    routes_resp = [
        RouteRateResponse(**row)
        for row in df.to_dict(orient="records")
    ]

    return RatesResponse(
        routes=routes_resp,
        average_rate_per_trip=result["avg_rate"],
        summary=SummaryStats(
            total_trips=result["total_trips"],
            total_route_costs=result["total_route_costs"],
            total_monthly_costs=result["total_monthly_costs"]
        )
    )


@app.get("/clients/scores", response_model=List[ClientScoreResponse], tags=["Predictive Engine"])
async def get_client_scores():
    df = predictive_engine.calculate_client_scores()
    if df.empty:
        raise BusinessLogicError("No client data available for scoring")

    return [ClientScoreResponse(**row) for row in df.to_dict(orient="records")]