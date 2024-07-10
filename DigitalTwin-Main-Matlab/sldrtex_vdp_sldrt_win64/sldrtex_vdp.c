/*
 * sldrtex_vdp.c
 *
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 *
 * Code generation for model "sldrtex_vdp".
 *
 * Model version              : 5.0
 * Simulink Coder version : 9.8 (R2022b) 13-May-2022
 * C source code generated on : Mon Mar 13 15:59:48 2023
 *
 * Target selection: sldrt.tlc
 * Note: GRT includes extra infrastructure and instrumentation for prototyping
 * Embedded hardware selection: Intel->x86-64 (Linux 64)
 * Code generation objectives: Unspecified
 * Validation result: Not run
 */

#include "sldrtex_vdp.h"
#include "sldrtex_vdp_private.h"
#include <string.h>
#include "rt_nonfinite.h"
#include "sldrtex_vdp_dt.h"

/* list of Simulink Desktop Real-Time timers */
const int SLDRTTimerCount = 1;
const double SLDRTTimers[2] = {
  0.0001, 0.0,
};

/* Block signals (default storage) */
B_sldrtex_vdp_T sldrtex_vdp_B;

/* Continuous states */
X_sldrtex_vdp_T sldrtex_vdp_X;

/* Block states (default storage) */
DW_sldrtex_vdp_T sldrtex_vdp_DW;

/* Real-time model */
static RT_MODEL_sldrtex_vdp_T sldrtex_vdp_M_;
RT_MODEL_sldrtex_vdp_T *const sldrtex_vdp_M = &sldrtex_vdp_M_;

/*
 * This function updates continuous states using the ODE5 fixed-step
 * solver algorithm
 */
static void rt_ertODEUpdateContinuousStates(RTWSolverInfo *si )
{
  /* Solver Matrices */
  static const real_T rt_ODE5_A[6] = {
    1.0/5.0, 3.0/10.0, 4.0/5.0, 8.0/9.0, 1.0, 1.0
  };

  static const real_T rt_ODE5_B[6][6] = {
    { 1.0/5.0, 0.0, 0.0, 0.0, 0.0, 0.0 },

    { 3.0/40.0, 9.0/40.0, 0.0, 0.0, 0.0, 0.0 },

    { 44.0/45.0, -56.0/15.0, 32.0/9.0, 0.0, 0.0, 0.0 },

    { 19372.0/6561.0, -25360.0/2187.0, 64448.0/6561.0, -212.0/729.0, 0.0, 0.0 },

    { 9017.0/3168.0, -355.0/33.0, 46732.0/5247.0, 49.0/176.0, -5103.0/18656.0,
      0.0 },

    { 35.0/384.0, 0.0, 500.0/1113.0, 125.0/192.0, -2187.0/6784.0, 11.0/84.0 }
  };

  time_T t = rtsiGetT(si);
  time_T tnew = rtsiGetSolverStopTime(si);
  time_T h = rtsiGetStepSize(si);
  real_T *x = rtsiGetContStates(si);
  ODE5_IntgData *id = (ODE5_IntgData *)rtsiGetSolverData(si);
  real_T *y = id->y;
  real_T *f0 = id->f[0];
  real_T *f1 = id->f[1];
  real_T *f2 = id->f[2];
  real_T *f3 = id->f[3];
  real_T *f4 = id->f[4];
  real_T *f5 = id->f[5];
  real_T hB[6];
  int_T i;
  int_T nXc = 2;
  rtsiSetSimTimeStep(si,MINOR_TIME_STEP);

  /* Save the state values at time t in y, we'll use x as ynew. */
  (void) memcpy(y, x,
                (uint_T)nXc*sizeof(real_T));

  /* Assumes that rtsiSetT and ModelOutputs are up-to-date */
  /* f0 = f(t,y) */
  rtsiSetdX(si, f0);
  sldrtex_vdp_derivatives();

  /* f(:,2) = feval(odefile, t + hA(1), y + f*hB(:,1), args(:)(*)); */
  hB[0] = h * rt_ODE5_B[0][0];
  for (i = 0; i < nXc; i++) {
    x[i] = y[i] + (f0[i]*hB[0]);
  }

  rtsiSetT(si, t + h*rt_ODE5_A[0]);
  rtsiSetdX(si, f1);
  sldrtex_vdp_output();
  sldrtex_vdp_derivatives();

  /* f(:,3) = feval(odefile, t + hA(2), y + f*hB(:,2), args(:)(*)); */
  for (i = 0; i <= 1; i++) {
    hB[i] = h * rt_ODE5_B[1][i];
  }

  for (i = 0; i < nXc; i++) {
    x[i] = y[i] + (f0[i]*hB[0] + f1[i]*hB[1]);
  }

  rtsiSetT(si, t + h*rt_ODE5_A[1]);
  rtsiSetdX(si, f2);
  sldrtex_vdp_output();
  sldrtex_vdp_derivatives();

  /* f(:,4) = feval(odefile, t + hA(3), y + f*hB(:,3), args(:)(*)); */
  for (i = 0; i <= 2; i++) {
    hB[i] = h * rt_ODE5_B[2][i];
  }

  for (i = 0; i < nXc; i++) {
    x[i] = y[i] + (f0[i]*hB[0] + f1[i]*hB[1] + f2[i]*hB[2]);
  }

  rtsiSetT(si, t + h*rt_ODE5_A[2]);
  rtsiSetdX(si, f3);
  sldrtex_vdp_output();
  sldrtex_vdp_derivatives();

  /* f(:,5) = feval(odefile, t + hA(4), y + f*hB(:,4), args(:)(*)); */
  for (i = 0; i <= 3; i++) {
    hB[i] = h * rt_ODE5_B[3][i];
  }

  for (i = 0; i < nXc; i++) {
    x[i] = y[i] + (f0[i]*hB[0] + f1[i]*hB[1] + f2[i]*hB[2] +
                   f3[i]*hB[3]);
  }

  rtsiSetT(si, t + h*rt_ODE5_A[3]);
  rtsiSetdX(si, f4);
  sldrtex_vdp_output();
  sldrtex_vdp_derivatives();

  /* f(:,6) = feval(odefile, t + hA(5), y + f*hB(:,5), args(:)(*)); */
  for (i = 0; i <= 4; i++) {
    hB[i] = h * rt_ODE5_B[4][i];
  }

  for (i = 0; i < nXc; i++) {
    x[i] = y[i] + (f0[i]*hB[0] + f1[i]*hB[1] + f2[i]*hB[2] +
                   f3[i]*hB[3] + f4[i]*hB[4]);
  }

  rtsiSetT(si, tnew);
  rtsiSetdX(si, f5);
  sldrtex_vdp_output();
  sldrtex_vdp_derivatives();

  /* tnew = t + hA(6);
     ynew = y + f*hB(:,6); */
  for (i = 0; i <= 5; i++) {
    hB[i] = h * rt_ODE5_B[5][i];
  }

  for (i = 0; i < nXc; i++) {
    x[i] = y[i] + (f0[i]*hB[0] + f1[i]*hB[1] + f2[i]*hB[2] +
                   f3[i]*hB[3] + f4[i]*hB[4] + f5[i]*hB[5]);
  }

  rtsiSetSimTimeStep(si,MAJOR_TIME_STEP);
}

/* Model output function */
void sldrtex_vdp_output(void)
{
  if (rtmIsMajorTimeStep(sldrtex_vdp_M)) {
    /* set solver stop time */
    if (!(sldrtex_vdp_M->Timing.clockTick0+1)) {
      rtsiSetSolverStopTime(&sldrtex_vdp_M->solverInfo,
                            ((sldrtex_vdp_M->Timing.clockTickH0 + 1) *
        sldrtex_vdp_M->Timing.stepSize0 * 4294967296.0));
    } else {
      rtsiSetSolverStopTime(&sldrtex_vdp_M->solverInfo,
                            ((sldrtex_vdp_M->Timing.clockTick0 + 1) *
        sldrtex_vdp_M->Timing.stepSize0 + sldrtex_vdp_M->Timing.clockTickH0 *
        sldrtex_vdp_M->Timing.stepSize0 * 4294967296.0));
    }
  }                                    /* end MajorTimeStep */

  /* Update absolute time of base rate at minor time step */
  if (rtmIsMinorTimeStep(sldrtex_vdp_M)) {
    sldrtex_vdp_M->Timing.t[0] = rtsiGetT(&sldrtex_vdp_M->solverInfo);
  }

  /* Integrator: '<Root>/Integrator1' */
  sldrtex_vdp_B.x1 = sldrtex_vdp_X.Integrator1_CSTATE;

  /* Integrator: '<Root>/Integrator2' */
  sldrtex_vdp_B.x2 = sldrtex_vdp_X.Integrator2_CSTATE;

  /* Saturate: '<Root>/Saturation' */
  if (sldrtex_vdp_B.x1 > sldrtex_vdp_P.Saturation_UpperSat) {
    /* Saturate: '<Root>/Saturation' */
    sldrtex_vdp_B.Saturation[0] = sldrtex_vdp_P.Saturation_UpperSat;
  } else if (sldrtex_vdp_B.x1 < sldrtex_vdp_P.Saturation_LowerSat) {
    /* Saturate: '<Root>/Saturation' */
    sldrtex_vdp_B.Saturation[0] = sldrtex_vdp_P.Saturation_LowerSat;
  } else {
    /* Saturate: '<Root>/Saturation' */
    sldrtex_vdp_B.Saturation[0] = sldrtex_vdp_B.x1;
  }

  if (sldrtex_vdp_B.x2 > sldrtex_vdp_P.Saturation_UpperSat) {
    /* Saturate: '<Root>/Saturation' */
    sldrtex_vdp_B.Saturation[1] = sldrtex_vdp_P.Saturation_UpperSat;
  } else if (sldrtex_vdp_B.x2 < sldrtex_vdp_P.Saturation_LowerSat) {
    /* Saturate: '<Root>/Saturation' */
    sldrtex_vdp_B.Saturation[1] = sldrtex_vdp_P.Saturation_LowerSat;
  } else {
    /* Saturate: '<Root>/Saturation' */
    sldrtex_vdp_B.Saturation[1] = sldrtex_vdp_B.x2;
  }

  /* End of Saturate: '<Root>/Saturation' */
  if (rtmIsMajorTimeStep(sldrtex_vdp_M)) {
  }

  /* Sum: '<Root>/Sum' incorporates:
   *  Constant: '<Root>/Constant'
   *  Gain: '<Root>/Mu'
   *  Math: '<Root>/Square'
   *  Product: '<Root>/Product'
   *  Sum: '<Root>/Sum1'
   */
  sldrtex_vdp_B.Sum = (sldrtex_vdp_P.Constant_Value - sldrtex_vdp_B.x1 *
                       sldrtex_vdp_B.x1) * sldrtex_vdp_B.x2 *
    sldrtex_vdp_P.Mu_Gain - sldrtex_vdp_B.x1;
  if (rtmIsMajorTimeStep(sldrtex_vdp_M)) {
    /* S-Function (sldrtsync): '<Root>/Real-Time Synchronization' */
    /* S-Function Block: <Root>/Real-Time Synchronization */
    {
      sldrtex_vdp_B.RealTimeSynchronization = 0;/* Missed Ticks value is always zero */
    }
  }
}

/* Model update function */
void sldrtex_vdp_update(void)
{
  if (rtmIsMajorTimeStep(sldrtex_vdp_M)) {
    rt_ertODEUpdateContinuousStates(&sldrtex_vdp_M->solverInfo);
  }

  /* Update absolute time for base rate */
  /* The "clockTick0" counts the number of times the code of this task has
   * been executed. The absolute time is the multiplication of "clockTick0"
   * and "Timing.stepSize0". Size of "clockTick0" ensures timer will not
   * overflow during the application lifespan selected.
   * Timer of this task consists of two 32 bit unsigned integers.
   * The two integers represent the low bits Timing.clockTick0 and the high bits
   * Timing.clockTickH0. When the low bit overflows to 0, the high bits increment.
   */
  if (!(++sldrtex_vdp_M->Timing.clockTick0)) {
    ++sldrtex_vdp_M->Timing.clockTickH0;
  }

  sldrtex_vdp_M->Timing.t[0] = rtsiGetSolverStopTime(&sldrtex_vdp_M->solverInfo);

  {
    /* Update absolute timer for sample time: [0.0001s, 0.0s] */
    /* The "clockTick1" counts the number of times the code of this task has
     * been executed. The absolute time is the multiplication of "clockTick1"
     * and "Timing.stepSize1". Size of "clockTick1" ensures timer will not
     * overflow during the application lifespan selected.
     * Timer of this task consists of two 32 bit unsigned integers.
     * The two integers represent the low bits Timing.clockTick1 and the high bits
     * Timing.clockTickH1. When the low bit overflows to 0, the high bits increment.
     */
    if (!(++sldrtex_vdp_M->Timing.clockTick1)) {
      ++sldrtex_vdp_M->Timing.clockTickH1;
    }

    sldrtex_vdp_M->Timing.t[1] = sldrtex_vdp_M->Timing.clockTick1 *
      sldrtex_vdp_M->Timing.stepSize1 + sldrtex_vdp_M->Timing.clockTickH1 *
      sldrtex_vdp_M->Timing.stepSize1 * 4294967296.0;
  }
}

/* Derivatives for root system: '<Root>' */
void sldrtex_vdp_derivatives(void)
{
  XDot_sldrtex_vdp_T *_rtXdot;
  _rtXdot = ((XDot_sldrtex_vdp_T *) sldrtex_vdp_M->derivs);

  /* Derivatives for Integrator: '<Root>/Integrator1' */
  _rtXdot->Integrator1_CSTATE = sldrtex_vdp_B.x2;

  /* Derivatives for Integrator: '<Root>/Integrator2' */
  _rtXdot->Integrator2_CSTATE = sldrtex_vdp_B.Sum;
}

/* Model initialize function */
void sldrtex_vdp_initialize(void)
{
  /* InitializeConditions for Integrator: '<Root>/Integrator1' */
  sldrtex_vdp_X.Integrator1_CSTATE = sldrtex_vdp_P.Integrator1_IC;

  /* InitializeConditions for Integrator: '<Root>/Integrator2' */
  sldrtex_vdp_X.Integrator2_CSTATE = sldrtex_vdp_P.Integrator2_IC;
}

/* Model terminate function */
void sldrtex_vdp_terminate(void)
{
  /* (no terminate code required) */
}

/*========================================================================*
 * Start of Classic call interface                                        *
 *========================================================================*/

/* Solver interface called by GRT_Main */
#ifndef USE_GENERATED_SOLVER

void rt_ODECreateIntegrationData(RTWSolverInfo *si)
{
  UNUSED_PARAMETER(si);
  return;
}                                      /* do nothing */

void rt_ODEDestroyIntegrationData(RTWSolverInfo *si)
{
  UNUSED_PARAMETER(si);
  return;
}                                      /* do nothing */

void rt_ODEUpdateContinuousStates(RTWSolverInfo *si)
{
  UNUSED_PARAMETER(si);
  return;
}                                      /* do nothing */

#endif

void MdlOutputs(int_T tid)
{
  sldrtex_vdp_output();
  UNUSED_PARAMETER(tid);
}

void MdlUpdate(int_T tid)
{
  sldrtex_vdp_update();
  UNUSED_PARAMETER(tid);
}

void MdlInitializeSizes(void)
{
}

void MdlInitializeSampleTimes(void)
{
}

void MdlInitialize(void)
{
}

void MdlStart(void)
{
  sldrtex_vdp_initialize();
}

void MdlTerminate(void)
{
  sldrtex_vdp_terminate();
}

/* Registration function */
RT_MODEL_sldrtex_vdp_T *sldrtex_vdp(void)
{
  /* Registration code */

  /* initialize non-finites */
  rt_InitInfAndNaN(sizeof(real_T));

  /* non-finite (run-time) assignments */
  sldrtex_vdp_P.RealTimeSynchronization_MaxMissedTicks = rtInf;

  /* initialize real-time model */
  (void) memset((void *)sldrtex_vdp_M, 0,
                sizeof(RT_MODEL_sldrtex_vdp_T));

  {
    /* Setup solver object */
    rtsiSetSimTimeStepPtr(&sldrtex_vdp_M->solverInfo,
                          &sldrtex_vdp_M->Timing.simTimeStep);
    rtsiSetTPtr(&sldrtex_vdp_M->solverInfo, &rtmGetTPtr(sldrtex_vdp_M));
    rtsiSetStepSizePtr(&sldrtex_vdp_M->solverInfo,
                       &sldrtex_vdp_M->Timing.stepSize0);
    rtsiSetdXPtr(&sldrtex_vdp_M->solverInfo, &sldrtex_vdp_M->derivs);
    rtsiSetContStatesPtr(&sldrtex_vdp_M->solverInfo, (real_T **)
                         &sldrtex_vdp_M->contStates);
    rtsiSetNumContStatesPtr(&sldrtex_vdp_M->solverInfo,
      &sldrtex_vdp_M->Sizes.numContStates);
    rtsiSetNumPeriodicContStatesPtr(&sldrtex_vdp_M->solverInfo,
      &sldrtex_vdp_M->Sizes.numPeriodicContStates);
    rtsiSetPeriodicContStateIndicesPtr(&sldrtex_vdp_M->solverInfo,
      &sldrtex_vdp_M->periodicContStateIndices);
    rtsiSetPeriodicContStateRangesPtr(&sldrtex_vdp_M->solverInfo,
      &sldrtex_vdp_M->periodicContStateRanges);
    rtsiSetErrorStatusPtr(&sldrtex_vdp_M->solverInfo, (&rtmGetErrorStatus
      (sldrtex_vdp_M)));
    rtsiSetRTModelPtr(&sldrtex_vdp_M->solverInfo, sldrtex_vdp_M);
  }

  rtsiSetSimTimeStep(&sldrtex_vdp_M->solverInfo, MAJOR_TIME_STEP);
  sldrtex_vdp_M->intgData.y = sldrtex_vdp_M->odeY;
  sldrtex_vdp_M->intgData.f[0] = sldrtex_vdp_M->odeF[0];
  sldrtex_vdp_M->intgData.f[1] = sldrtex_vdp_M->odeF[1];
  sldrtex_vdp_M->intgData.f[2] = sldrtex_vdp_M->odeF[2];
  sldrtex_vdp_M->intgData.f[3] = sldrtex_vdp_M->odeF[3];
  sldrtex_vdp_M->intgData.f[4] = sldrtex_vdp_M->odeF[4];
  sldrtex_vdp_M->intgData.f[5] = sldrtex_vdp_M->odeF[5];
  sldrtex_vdp_M->contStates = ((real_T *) &sldrtex_vdp_X);
  rtsiSetSolverData(&sldrtex_vdp_M->solverInfo, (void *)&sldrtex_vdp_M->intgData);
  rtsiSetIsMinorTimeStepWithModeChange(&sldrtex_vdp_M->solverInfo, false);
  rtsiSetSolverName(&sldrtex_vdp_M->solverInfo,"ode5");

  /* Initialize timing info */
  {
    int_T *mdlTsMap = sldrtex_vdp_M->Timing.sampleTimeTaskIDArray;
    mdlTsMap[0] = 0;
    mdlTsMap[1] = 1;

    /* polyspace +2 MISRA2012:D4.1 [Justified:Low] "sldrtex_vdp_M points to
       static memory which is guaranteed to be non-NULL" */
    sldrtex_vdp_M->Timing.sampleTimeTaskIDPtr = (&mdlTsMap[0]);
    sldrtex_vdp_M->Timing.sampleTimes = (&sldrtex_vdp_M->
      Timing.sampleTimesArray[0]);
    sldrtex_vdp_M->Timing.offsetTimes = (&sldrtex_vdp_M->
      Timing.offsetTimesArray[0]);

    /* task periods */
    sldrtex_vdp_M->Timing.sampleTimes[0] = (0.0);
    sldrtex_vdp_M->Timing.sampleTimes[1] = (0.0001);

    /* task offsets */
    sldrtex_vdp_M->Timing.offsetTimes[0] = (0.0);
    sldrtex_vdp_M->Timing.offsetTimes[1] = (0.0);
  }

  rtmSetTPtr(sldrtex_vdp_M, &sldrtex_vdp_M->Timing.tArray[0]);

  {
    int_T *mdlSampleHits = sldrtex_vdp_M->Timing.sampleHitArray;
    mdlSampleHits[0] = 1;
    mdlSampleHits[1] = 1;
    sldrtex_vdp_M->Timing.sampleHits = (&mdlSampleHits[0]);
  }

  rtmSetTFinal(sldrtex_vdp_M, 10.0);
  sldrtex_vdp_M->Timing.stepSize0 = 0.0001;
  sldrtex_vdp_M->Timing.stepSize1 = 0.0001;

  /* External mode info */
  sldrtex_vdp_M->Sizes.checksums[0] = (578503360U);
  sldrtex_vdp_M->Sizes.checksums[1] = (721547871U);
  sldrtex_vdp_M->Sizes.checksums[2] = (2059394663U);
  sldrtex_vdp_M->Sizes.checksums[3] = (56234064U);

  {
    static const sysRanDType rtAlwaysEnabled = SUBSYS_RAN_BC_ENABLE;
    static RTWExtModeInfo rt_ExtModeInfo;
    static const sysRanDType *systemRan[1];
    sldrtex_vdp_M->extModeInfo = (&rt_ExtModeInfo);
    rteiSetSubSystemActiveVectorAddresses(&rt_ExtModeInfo, systemRan);
    systemRan[0] = &rtAlwaysEnabled;
    rteiSetModelMappingInfoPtr(sldrtex_vdp_M->extModeInfo,
      &sldrtex_vdp_M->SpecialInfo.mappingInfo);
    rteiSetChecksumsPtr(sldrtex_vdp_M->extModeInfo,
                        sldrtex_vdp_M->Sizes.checksums);
    rteiSetTPtr(sldrtex_vdp_M->extModeInfo, rtmGetTPtr(sldrtex_vdp_M));
  }

  sldrtex_vdp_M->solverInfoPtr = (&sldrtex_vdp_M->solverInfo);
  sldrtex_vdp_M->Timing.stepSize = (0.0001);
  rtsiSetFixedStepSize(&sldrtex_vdp_M->solverInfo, 0.0001);
  rtsiSetSolverMode(&sldrtex_vdp_M->solverInfo, SOLVER_MODE_SINGLETASKING);

  /* block I/O */
  sldrtex_vdp_M->blockIO = ((void *) &sldrtex_vdp_B);
  (void) memset(((void *) &sldrtex_vdp_B), 0,
                sizeof(B_sldrtex_vdp_T));

  {
    sldrtex_vdp_B.x1 = 0.0;
    sldrtex_vdp_B.x2 = 0.0;
    sldrtex_vdp_B.Saturation[0] = 0.0;
    sldrtex_vdp_B.Saturation[1] = 0.0;
    sldrtex_vdp_B.Sum = 0.0;
  }

  /* parameters */
  sldrtex_vdp_M->defaultParam = ((real_T *)&sldrtex_vdp_P);

  /* states (continuous) */
  {
    real_T *x = (real_T *) &sldrtex_vdp_X;
    sldrtex_vdp_M->contStates = (x);
    (void) memset((void *)&sldrtex_vdp_X, 0,
                  sizeof(X_sldrtex_vdp_T));
  }

  /* states (dwork) */
  sldrtex_vdp_M->dwork = ((void *) &sldrtex_vdp_DW);
  (void) memset((void *)&sldrtex_vdp_DW, 0,
                sizeof(DW_sldrtex_vdp_T));

  /* data type transition information */
  {
    static DataTypeTransInfo dtInfo;
    (void) memset((char_T *) &dtInfo, 0,
                  sizeof(dtInfo));
    sldrtex_vdp_M->SpecialInfo.mappingInfo = (&dtInfo);
    dtInfo.numDataTypes = 23;
    dtInfo.dataTypeSizes = &rtDataTypeSizes[0];
    dtInfo.dataTypeNames = &rtDataTypeNames[0];

    /* Block I/O transition table */
    dtInfo.BTransTable = &rtBTransTable;

    /* Parameters transition table */
    dtInfo.PTransTable = &rtPTransTable;
  }

  /* Initialize Sizes */
  sldrtex_vdp_M->Sizes.numContStates = (2);/* Number of continuous states */
  sldrtex_vdp_M->Sizes.numPeriodicContStates = (0);
                                      /* Number of periodic continuous states */
  sldrtex_vdp_M->Sizes.numY = (0);     /* Number of model outputs */
  sldrtex_vdp_M->Sizes.numU = (0);     /* Number of model inputs */
  sldrtex_vdp_M->Sizes.sysDirFeedThru = (0);/* The model is not direct feedthrough */
  sldrtex_vdp_M->Sizes.numSampTimes = (2);/* Number of sample times */
  sldrtex_vdp_M->Sizes.numBlocks = (12);/* Number of blocks */
  sldrtex_vdp_M->Sizes.numBlockIO = (5);/* Number of block outputs */
  sldrtex_vdp_M->Sizes.numBlockPrms = (8);/* Sum of parameter "widths" */
  return sldrtex_vdp_M;
}

/*========================================================================*
 * End of Classic call interface                                          *
 *========================================================================*/
