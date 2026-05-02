"""Main workflow orchestration logic"""

import logging
from typing import Any, Dict, Optional

from app.agents.diagnoser import DiagnoserAgent
from app.agents.fixer import FixerAgent
from app.pipeline.ingestion import WorkflowIngestion
from app.pipeline.static_analysis import StaticAnalyzer
from app.pipeline.validation import WorkflowValidator

logger = logging.getLogger(__name__)


class WorkflowOrchestrator:
    """Orchestrates the workflow analysis and optimization pipeline"""
    
    def __init__(self):
        self.ingestion = WorkflowIngestion()
        self.static_analyzer = StaticAnalyzer()
        self.diagnoser = DiagnoserAgent()
        self.fixer = FixerAgent()
        self.validator = WorkflowValidator()
        # In-memory storage for analysis results (TODO: replace with Redis/DB)
        self._analysis_cache: Dict[str, Any] = {}
        self._fix_cache: Dict[str, Any] = {}
    
    async def analyze_workflow(
        self,
        workflow_input: str,
        source_type: str,
        analysis_id: str
    ) -> Dict[str, Any]:
        """
        Analyze a workflow to identify optimization opportunities.
        
        Args:
            workflow_input: Workflow content or repository URL
            source_type: Type of input (text, github, file)
            analysis_id: Unique analysis identifier
        
        Returns:
            Analysis results with bottlenecks and recommendations
        """
        logger.info(f"Starting workflow analysis: {analysis_id}")
        
        try:
            # Step 1: Ingest and normalize workflow
            logger.debug("Ingesting workflow...")
            workflow_data = await self.ingestion.ingest(workflow_input, source_type)
            
            # Step 2: Static analysis
            logger.debug("Performing static analysis...")
            static_results = await self.static_analyzer.analyze(workflow_data)
            
            # Step 3: AI-powered diagnosis
            logger.debug("Running AI diagnosis...")
            diagnosis = await self.diagnoser.diagnose(workflow_data, static_results)
            
            # Step 4: Store workflow data for later use in fix generation
            self._analysis_cache[analysis_id] = {
                "workflow_data": workflow_data,
                "static_results": static_results,
                "diagnosis": diagnosis
            }
            logger.debug(f"Stored analysis data for {analysis_id}")
            
            # Step 5: Compile results
            results = {
                "workflow_structure": diagnosis.get("workflow_structure", workflow_data.get("structure")),
                "bottlenecks": diagnosis.get("bottlenecks", []),
                "metrics": {
                    "current_duration": diagnosis.get("current_duration", "Unknown"),
                    "estimated_optimal": diagnosis.get("estimated_optimal", "Unknown"),
                    "efficiency_score": diagnosis.get("efficiency_score", 0)
                },
                "recommendations": diagnosis.get("recommendations", []),
                "estimated_improvement": diagnosis.get("estimated_improvement", "0%")
            }
            
            logger.info(f"Analysis results - Bottlenecks: {len(results['bottlenecks'])}, Duration: {results['metrics']['current_duration']} -> {results['metrics']['estimated_optimal']}")
            
            logger.info(f"Analysis completed: {analysis_id}")
            return results
            
        except Exception as e:
            logger.error(f"Analysis failed: {str(e)}")
            raise
    
    async def generate_fix(
        self,
        analysis_id: str,
        optimization_strategy: str,
        fix_id: str
    ) -> Dict[str, Any]:
        """
        Generate an optimized workflow based on analysis.
        
        Args:
            analysis_id: Analysis identifier
            optimization_strategy: Strategy to use (aggressive, balanced, conservative)
            fix_id: Unique fix identifier
        
        Returns:
            Optimized workflow and improvements
        """
        logger.info(f"Generating fix: {fix_id} for analysis: {analysis_id}")
        
        try:
            # Retrieve analysis results from storage
            analysis_data = self._analysis_cache.get(analysis_id)
            workflow_data = analysis_data.get("workflow_data") if analysis_data else None
            
            # Step 1: Generate optimized workflow
            logger.debug("Generating optimized workflow...")
            optimized = await self.fixer.generate_fix(
                analysis_id=analysis_id,
                strategy=optimization_strategy,
                workflow_data=workflow_data
            )
            
            # Step 2: Validate optimized workflow
            logger.debug("Validating optimized workflow...")
            workflow_to_validate = optimized.get("workflow", {})
            validation = await self.validator.validate(workflow_to_validate)
            
            if not validation.get("valid"):
                raise ValueError(f"Generated workflow is invalid: {validation.get('errors')}")
            
            # Step 3: Store fix data for PR creation
            self._fix_cache[fix_id] = optimized
            logger.debug(f"Stored fix data for {fix_id}")
            
            # Step 4: Compile results
            results = {
                "optimized_workflow": optimized.get("workflow"),
                "workflow_yaml": optimized.get("workflow_yaml"),
                "changes": optimized.get("changes", []),
                "improvements": {
                    "time_saved": optimized.get("time_saved", "Unknown"),
                    "efficiency_gain": optimized.get("efficiency_gain", "0%"),
                    "optimizations_applied": len(optimized.get("changes", []))
                },
                "diff": optimized.get("diff", "")
            }
            
            logger.info(f"Fix generated: {fix_id}")
            return results
            
        except Exception as e:
            logger.error(f"Fix generation failed: {str(e)}")
            raise

# Made with Bob
