//----------Author's Name:F.X. Gentit  DAPNIA/SPP CEN Saclay
//----------Copyright:Those valid for CEA sofware
//----------Modified:07/06/2007

#include "CalibCalorimetry/EcalCorrelatedNoiseAnalysisAlgos/interface/TNArrayD.h"
//#include "Riostream.h"

ClassImp(TNArrayD)
//______________________________________________________________________________
//
// TNArrayD  ROOT class for multidimensional arrays of Double_t
//
//   up to dimension 6
//   book one place more for overflow
//   detects overflow
//
TNArrayD::TNArrayD(const TNArrayD &orig) {
//copy constructor
  fNd = orig.fNd;
  fN1 = orig.fN1;
  fN2 = orig.fN2;
  fN3 = orig.fN3;
  fN4 = orig.fN4;
  fN5 = orig.fN5;
  fN6 = orig.fN6;
  fNL = orig.fNL;
  fA  = new Double_t [fNL];
  for (Int_t i=0;i<fNL;i++) fA[i] = orig.fA[i];
}
TNArrayD::TNArrayD(Int_t n1) {
//constructor for a 1 dimensional array of size n1. Array is put to 0
  const Double_t zero = 0.0;
  Init();
  fNd  = 1;
  fN1  = n1;
  fNL  = n1 + 1;
  fA   = new Double_t [fNL];
  for (Int_t i=0;i<fNL;i++) fA[i] = zero;
}
TNArrayD::TNArrayD(Int_t n1,Int_t n2) {
//constructor for a 2 dimensional array of sizes n1,n2. Array is put to 0
  const Double_t zero = 0.0;
  Init();
  fNd = 2;
  fN1 = n1;
  fN2 = n2;
  fNL = n1*n2 + 1;
  fA  = new Double_t [fNL];
  for (Int_t i=0;i<fNL;i++) fA[i] = zero;
}
TNArrayD::TNArrayD(Int_t n1,Int_t n2,Int_t n3) {
//constructor 3 dimensional array of sizes n1,n2,n3. Array is put to 0
  const Double_t zero = 0.0;
  Init();
  fNd  = 3;
  fN1  = n1;
  fN2  = n2;
  fN3  = n3;
  fNL  = n1*n2*n3 + 1;
  fA   = new Double_t [fNL];
  for (Int_t i=0;i<fNL;i++) fA[i] = zero;
}
TNArrayD::TNArrayD(Int_t n1,Int_t n2,Int_t n3,Int_t n4) {
//constructor for a 4 dimensional array of sizes n1,n2,n3,n4. Array is put to 0
  const Double_t zero = 0.0;
  Init();
  fNd  = 4;
  fN1  = n1;
  fN2  = n2;
  fN3  = n3;
  fN4  = n4;
  fNL  = n1*n2*n3*n4 + 1;
  fA   = new Double_t [fNL];
  for (Int_t i=0;i<fNL;i++) fA[i] = zero;
}
TNArrayD::TNArrayD(Int_t n1,Int_t n2,Int_t n3,Int_t n4,Int_t n5) {
//constructor for a 5 dimensional array of sizes n1,n2,n3,n4,n5. Array is put to 0
  const Double_t zero = 0.0;
  Init();
  fNd  = 5;
  fN1  = n1;
  fN2  = n2;
  fN3  = n3;
  fN4  = n4;
  fN5  = n5;
  fNL  = n1*n2*n3*n4*n5 + 1;
  fA   = new Double_t [fNL];
  for (Int_t i=0;i<fNL;i++) fA[i] = zero;
}
TNArrayD::TNArrayD(Int_t n1,Int_t n2,Int_t n3,Int_t n4,Int_t n5,Int_t n6) {
//constructor for a 6 dimensional array of sizes n1,n2,n3,n4,n5,n6. Array is put to 0
  const Double_t zero = 0.0;
  Init();
  fNd  = 6;
  fN1  = n1;
  fN2  = n2;
  fN3  = n3;
  fN4  = n4;
  fN5  = n5;
  fN6  = n6;
  fNL  = n1*n2*n3*n4*n5*n6 + 1;
  fA   = new Double_t [fNL];
  for (Int_t i=0;i<fNL;i++) fA[i] = zero;
}
TNArrayD::~TNArrayD() {
//destructor
  Clean();
}
void TNArrayD::Clean() {
//
  if (fA) delete [] fA;
  Init();
}
void TNArrayD::Init() {
//Initialization
  fNd  = 0;
  fN1  = 1;
  fN2  = 1;
  fN3  = 1;
  fN4  = 1;
  fN5  = 1;
  fN6  = 1;
  fNL  = 0;
  fA   = 0;
}
inline Int_t TNArrayD::OneDim(Int_t i1) const {
//Index from 1 dimension to 1 dimension
  if ((i1>=fNL - 1) || (i1<0)) {
    i1 = fNL - 1;
    Error("OneDim","Index outside bounds");
    //cout << "i1  = " << i1
    // << "; fNL = " << fNL << endl;
  }
  return i1;
}
inline Int_t TNArrayD::OneDim(Int_t i1,Int_t i2) const {
//Index from 2 dimension to 1 dimension
  Int_t i;
  i = i1 + fN1*i2;
  if ((i>=fNL - 1) || (i<0)) {
    i = fNL - 1;
    Error("OneDim","Index outside bounds");
    //cout << "i1  = " << i1  << ", i2 = "  << i2
    //	 << "; fN1 = " << fN1 << ", fNL = " << fNL << endl;
  }
  return i;
}
inline Int_t TNArrayD::OneDim(Int_t i1,Int_t i2,Int_t i3) const {
//Index from 3 dimension to 1 dimension
  Int_t i;
  i = i1 + fN1*(i2 + fN2*i3);
  if ((i>=fNL - 1) || (i<0)) {
    i = fNL - 1;
    Error("OneDim","Index outside bounds");
    //cout << "i1  = " << i1  << ", i2 = "  << i2  << ", i3 = "  << i3
    // << "; fN1 = " << fN1 << ", fN2 = " << fN2 << ", fNL = " << fNL << endl;
  }
  return i;
}
inline Int_t TNArrayD::OneDim(Int_t i1,Int_t i2,Int_t i3,Int_t i4) const {
//Index from 4 dimension to 1 dimension
  Int_t i;
  i = i1 + fN1*(i2 + fN2*(i3 + fN3*i4));
  if ((i>=fNL - 1) || (i<0)) {
    i = fNL - 1;
    Error("OneDim","Index outside bounds");
  }
  return i;
}
inline Int_t TNArrayD::OneDim(Int_t i1,Int_t i2,Int_t i3,Int_t i4,Int_t i5) const {
//Index from 5 dimension to 1 dimension
  Int_t i;
  i = i1 + fN1*(i2 + fN2*(i3 + fN3*(i4 + fN4*i5)));
  if ((i>=fNL - 1) || (i<0)) {
    i = fNL - 1;
    Error("OneDim","Index outside bounds");
  }
  return i;
}
inline Int_t TNArrayD::OneDim(Int_t i1,Int_t i2,Int_t i3,Int_t i4,Int_t i5,Int_t i6) const {
//Index from 6 dimension to 1 dimension
  Int_t i;
  i = i1 + fN1*(i2 + fN2*(i3 + fN3*(i4 + fN4*(i5 + fN5*i6))));
  if ((i>=fNL - 1) || (i<0)) {
    i = fNL - 1;
    Error("OneDim","Index outside bounds");
  }
  return i;
}
void TNArrayD::ReSet(Int_t n1) {
//Reset this to be 1 dimensional of dimension n1
  const Double_t zero = 0.0;
  Clean();
  fNd  = 1;
  fN1  = n1;
  fNL  = n1 + 1;
  fA   = new Double_t [fNL];
  for (Int_t i=0;i<fNL;i++) fA[i] = zero;
}
void TNArrayD::ReSet(Int_t n1,Int_t n2) {
//Reset this to be 2 dimensional of dimension n1,n2
  const Double_t zero = 0.0;
  Clean();
  fNd  = 2;
  fN1  = n1;
  fN2  = n2;
  fNL  = n1*n2 + 1;
  fA   = new Double_t [fNL];
  for (Int_t i=0;i<fNL;i++) fA[i] = zero;
}
void TNArrayD::ReSet(Int_t n1,Int_t n2,Int_t n3) {
//Reset this to be 3 dimensional of dimension n1,n2,n3
  const Double_t zero = 0.0;
  Clean();
  fNd  = 3;
  fN1  = n1;
  fN2  = n2;
  fN3  = n3;
  fNL  = n1*n2*n3 + 1;
  fA   = new Double_t [fNL];
  for (Int_t i=0;i<fNL;i++) fA[i] = zero;
}
void TNArrayD::ReSet(Int_t n1,Int_t n2,Int_t n3,Int_t n4) {
//Reset this to be 4 dimensional of dimension n1,n2,n3,n4
  const Double_t zero = 0.0;
  Clean();
  fNd  = 4;
  fN1  = n1;
  fN2  = n2;
  fN3  = n3;
  fN4  = n4;
  fNL  = n1*n2*n3*n4 + 1;
  fA   = new Double_t [fNL];
  for (Int_t i=0;i<fNL;i++) fA[i] = zero;
}
void TNArrayD::ReSet(Int_t n1,Int_t n2,Int_t n3,Int_t n4,Int_t n5) {
//Reset this to be 5 dimensional of dimension n1,n2,n3,n4,n5
  const Double_t zero = 0.0;
  Clean();
  fNd  = 5;
  fN1  = n1;
  fN2  = n2;
  fN3  = n3;
  fN4  = n4;
  fN5  = n5;
  fNL  = n1*n2*n3*n4*n5 + 1;
  fA   = new Double_t [fNL];
  for (Int_t i=0;i<fNL;i++) fA[i] = zero;
}
void TNArrayD::ReSet(Int_t n1,Int_t n2,Int_t n3,Int_t n4,Int_t n5,Int_t n6) {
//Reset this to be 6 dimensional of dimension n1,n2,n3,n4,n5,n6
  const Double_t zero = 0.0;
  Clean();
  fNd  = 6;
  fN1  = n1;
  fN2  = n2;
  fN3  = n3;
  fN4  = n4;
  fN5  = n5;
  fN6  = n6;
  fNL  = n1*n2*n3*n4*n5*n6 + 1;
  fA   = new Double_t [fNL];
  for (Int_t i=0;i<fNL;i++) fA[i] = zero;
}
const Double_t &TNArrayD::operator()(Int_t i1) const {
  Int_t i;
  i = OneDim(i1);
  return fA[i];
}
const Double_t &TNArrayD::operator()(Int_t i1,Int_t i2) const {
  Int_t i;
  i = OneDim(i1,i2);
  return fA[i];
}
const Double_t &TNArrayD::operator()(Int_t i1,Int_t i2,Int_t i3) const {
  Int_t i;
  i = OneDim(i1,i2,i3);
  return fA[i];
}
const Double_t &TNArrayD::operator()(Int_t i1,Int_t i2,Int_t i3,Int_t i4) const {
  Int_t i;
  i = OneDim(i1,i2,i3,i4);
  return fA[i];
}
const Double_t &TNArrayD::operator()(Int_t i1,Int_t i2,Int_t i3,Int_t i4,Int_t i5) const {
  Int_t i;
  i = OneDim(i1,i2,i3,i4,i5);
  return fA[i];
}
const Double_t &TNArrayD::operator()(Int_t i1,Int_t i2,Int_t i3,Int_t i4,Int_t i5,Int_t i6) const {
  Int_t i;
  i = OneDim(i1,i2,i3,i4,i5,i6);
  return fA[i];
}
Double_t &TNArrayD::operator()(Int_t i1)
{
   return (Double_t&)((*(const TNArrayD *)this)(i1));
}
Double_t &TNArrayD::operator()(Int_t i1,Int_t i2)
{
   return (Double_t&)((*(const TNArrayD *)this)(i1,i2));
}
Double_t &TNArrayD::operator()(Int_t i1,Int_t i2,Int_t i3)
{
   return (Double_t&)((*(const TNArrayD *)this)(i1,i2,i3));
}
Double_t &TNArrayD::operator()(Int_t i1,Int_t i2,Int_t i3,Int_t i4)
{
   return (Double_t&)((*(const TNArrayD *)this)(i1,i2,i3,i4));
}
Double_t &TNArrayD::operator()(Int_t i1,Int_t i2,Int_t i3,Int_t i4,Int_t i5)
{
   return (Double_t&)((*(const TNArrayD *)this)(i1,i2,i3,i4,i5));
}
Double_t &TNArrayD::operator()(Int_t i1,Int_t i2,Int_t i3,Int_t i4,Int_t i5,Int_t i6)
{
   return (Double_t&)((*(const TNArrayD *)this)(i1,i2,i3,i4,i5,i6));
}

