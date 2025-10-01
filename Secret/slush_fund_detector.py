import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Any
import re
from dataclasses import dataclass
from enum import Enum
import logging

class RiskLevel(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4

@dataclass
class Alert:
    account_id: str
    alert_type: str
    risk_level: RiskLevel
    confidence_score: float
    description: str
    evidence: List[str]
    timestamp: datetime
    amount_involved: float = 0.0

class SlushFundDetector:
    """
    Advanced slush fund detection system for banking institutions.
    Analyzes transaction patterns, account behaviors, and relationships
    to identify potential slush fund activities.
    """
    
    def __init__(self):
        self.setup_logging()
        self.suspicious_keywords = [
            'consulting', 'advisory', 'services', 'misc', 'miscellaneous',
            'general', 'expenses', 'petty cash', 'discretionary', 'contingency',
            'emergency', 'special projects', 'undefined', 'various',
            'entertainment', 'representation', 'goodwill', 'hospitality'
        ]
        
        self.high_risk_industries = [
            'consulting', 'advisory services', 'shell companies',
            'offshore entities', 'holding companies'
        ]
        
    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
    
    def analyze_account(self, transactions_df: pd.DataFrame, 
                       account_info: Dict[str, Any]) -> List[Alert]:
        """
        Main analysis function that runs all detection algorithms
        """
        alerts = []
        account_id = account_info.get('account_id', 'unknown')
        
        # Run all detection methods
        alerts.extend(self.detect_round_number_patterns(transactions_df, account_id))
        alerts.extend(self.detect_suspicious_descriptions(transactions_df, account_id))
        alerts.extend(self.detect_unusual_frequency_patterns(transactions_df, account_id))
        alerts.extend(self.detect_threshold_avoidance(transactions_df, account_id))
        alerts.extend(self.detect_end_of_period_activities(transactions_df, account_id))
        alerts.extend(self.detect_unusual_counterparties(transactions_df, account_id))
        alerts.extend(self.detect_cash_intensive_patterns(transactions_df, account_id))
        alerts.extend(self.detect_layering_patterns(transactions_df, account_id))
        
        return self.prioritize_alerts(alerts)
    
    def detect_round_number_patterns(self, df: pd.DataFrame, account_id: str) -> List[Alert]:
        """
        Detect suspicious patterns in round number transactions
        """
        alerts = []
        
        # Check for excessive round numbers
        round_numbers = df[df['amount'].apply(lambda x: x % 100 == 0 or x % 50 == 0)]
        total_transactions = len(df)
        
        if total_transactions > 10:  # Only analyze accounts with sufficient activity
            round_percentage = len(round_numbers) / total_transactions
            
            if round_percentage > 0.6:  # More than 60% round numbers
                evidence = [
                    f"{len(round_numbers)} out of {total_transactions} transactions are round numbers",
                    f"Round number percentage: {round_percentage:.2%}"
                ]
                
                alerts.append(Alert(
                    account_id=account_id,
                    alert_type="Round Number Pattern",
                    risk_level=RiskLevel.MEDIUM if round_percentage < 0.8 else RiskLevel.HIGH,
                    confidence_score=min(round_percentage * 100, 95),
                    description="Unusually high percentage of round-number transactions",
                    evidence=evidence,
                    timestamp=datetime.now(),
                    amount_involved=round_numbers['amount'].sum()
                ))
        
        return alerts
    
    def detect_suspicious_descriptions(self, df: pd.DataFrame, account_id: str) -> List[Alert]:
        """
        Analyze transaction descriptions for suspicious patterns
        """
        alerts = []
        
        if 'description' not in df.columns:
            return alerts
        
        # Check for vague descriptions
        vague_descriptions = df[df['description'].str.lower().str.contains(
            '|'.join(self.suspicious_keywords), na=False, regex=True
        )]
        
        if len(vague_descriptions) > len(df) * 0.3:  # More than 30% vague descriptions
            evidence = [
                f"Found {len(vague_descriptions)} transactions with vague descriptions",
                f"Common suspicious keywords: {', '.join(set(vague_descriptions['description'].str.lower().str.extract('(' + '|'.join(self.suspicious_keywords) + ')', expand=False).dropna()))}"
            ]
            
            alerts.append(Alert(
                account_id=account_id,
                alert_type="Vague Transaction Descriptions",
                risk_level=RiskLevel.MEDIUM,
                confidence_score=75,
                description="High frequency of vague or generic transaction descriptions",
                evidence=evidence,
                timestamp=datetime.now(),
                amount_involved=vague_descriptions['amount'].sum()
            ))
        
        # Check for identical descriptions
        description_counts = df['description'].value_counts()
        repeated_descriptions = description_counts[description_counts > 5]
        
        if len(repeated_descriptions) > 0:
            evidence = [f"Description '{desc}' appears {count} times" 
                       for desc, count in repeated_descriptions.head(5).items()]
            
            alerts.append(Alert(
                account_id=account_id,
                alert_type="Repeated Transaction Descriptions",
                risk_level=RiskLevel.MEDIUM,
                confidence_score=60,
                description="Multiple transactions with identical descriptions",
                evidence=evidence,
                timestamp=datetime.now()
            ))
        
        return alerts
    
    def detect_threshold_avoidance(self, df: pd.DataFrame, account_id: str) -> List[Alert]:
        """
        Detect transactions that appear to avoid reporting thresholds
        """
        alerts = []
        
        # Common reporting thresholds
        thresholds = [10000, 5000, 3000, 1000]
        
        for threshold in thresholds:
            # Look for transactions just below threshold
            near_threshold = df[
                (df['amount'] >= threshold * 0.9) & 
                (df['amount'] < threshold)
            ]
            
            if len(near_threshold) > 3:  # Multiple transactions near threshold
                evidence = [
                    f"{len(near_threshold)} transactions between ${threshold * 0.9:,.0f} and ${threshold:,.0f}",
                    f"Average amount: ${near_threshold['amount'].mean():,.2f}"
                ]
                
                risk_level = RiskLevel.HIGH if threshold >= 10000 else RiskLevel.MEDIUM
                
                alerts.append(Alert(
                    account_id=account_id,
                    alert_type="Threshold Avoidance",
                    risk_level=risk_level,
                    confidence_score=80,
                    description=f"Multiple transactions appear to avoid ${threshold:,} reporting threshold",
                    evidence=evidence,
                    timestamp=datetime.now(),
                    amount_involved=near_threshold['amount'].sum()
                ))
        
        return alerts
    
    def detect_unusual_frequency_patterns(self, df: pd.DataFrame, account_id: str) -> List[Alert]:
        """
        Detect unusual patterns in transaction timing and frequency
        """
        alerts = []
        
        if 'date' not in df.columns:
            return alerts
        
        # Ensure date column is datetime
        df['date'] = pd.to_datetime(df['date'])
        
        # Check for burst patterns (many transactions in short periods)
        df_sorted = df.sort_values('date')
        df_sorted['days_since_last'] = df_sorted['date'].diff().dt.days
        
        # Find periods with high transaction density
        recent_activity = df_sorted[df_sorted['days_since_last'] <= 1]
        
        if len(recent_activity) > len(df) * 0.4:  # More than 40% within 1 day of each other
            evidence = [
                f"{len(recent_activity)} transactions occurred within 1 day of another transaction",
                f"Indicates potential burst activity pattern"
            ]
            
            alerts.append(Alert(
                account_id=account_id,
                alert_type="Burst Transaction Pattern",
                risk_level=RiskLevel.MEDIUM,
                confidence_score=65,
                description="Unusual concentration of transactions in short time periods",
                evidence=evidence,
                timestamp=datetime.now()
            ))
        
        return alerts
    
    def detect_end_of_period_activities(self, df: pd.DataFrame, account_id: str) -> List[Alert]:
        """
        Detect suspicious end-of-month/quarter/year activities
        """
        alerts = []
        
        if 'date' not in df.columns:
            return alerts
        
        df['date'] = pd.to_datetime(df['date'])
        df['day_of_month'] = df['date'].dt.day
        df['month'] = df['date'].dt.month
        
        # Check for end-of-month clustering (last 3 days)
        end_of_month = df[df['day_of_month'] >= 28]
        
        if len(end_of_month) > len(df) * 0.25:  # More than 25% at month-end
            evidence = [
                f"{len(end_of_month)} transactions occur in last 3 days of month",
                f"End-of-month transaction percentage: {len(end_of_month)/len(df):.2%}"
            ]
            
            alerts.append(Alert(
                account_id=account_id,
                alert_type="End-of-Period Clustering",
                risk_level=RiskLevel.MEDIUM,
                confidence_score=70,
                description="Unusual concentration of transactions at month-end",
                evidence=evidence,
                timestamp=datetime.now(),
                amount_involved=end_of_month['amount'].sum()
            ))
        
        # Check for year-end/quarter-end patterns
        quarter_ends = df[df['month'].isin([3, 6, 9, 12])]
        if len(quarter_ends) > len(df) * 0.4:
            evidence = [f"High concentration of transactions at quarter-ends: {len(quarter_ends)} transactions"]
            
            alerts.append(Alert(
                account_id=account_id,
                alert_type="Quarter-End Pattern",
                risk_level=RiskLevel.MEDIUM,
                confidence_score=65,
                description="Unusual pattern of quarter-end transactions",
                evidence=evidence,
                timestamp=datetime.now()
            ))
        
        return alerts
    
    def detect_unusual_counterparties(self, df: pd.DataFrame, account_id: str) -> List[Alert]:
        """
        Detect suspicious counterparty patterns
        """
        alerts = []
        
        if 'counterparty' not in df.columns:
            return alerts
        
        # Check for high concentration with few counterparties
        counterparty_counts = df['counterparty'].value_counts()
        total_amount_by_counterparty = df.groupby('counterparty')['amount'].sum().sort_values(ascending=False)
        
        # Top counterparty concentration
        if len(counterparty_counts) > 0:
            top_counterparty_share = total_amount_by_counterparty.iloc[0] / df['amount'].sum()
            
            if top_counterparty_share > 0.5:  # One counterparty represents >50% of volume
                evidence = [
                    f"Top counterparty accounts for {top_counterparty_share:.2%} of total transaction volume",
                    f"Counterparty: {total_amount_by_counterparty.index[0]}"
                ]
                
                alerts.append(Alert(
                    account_id=account_id,
                    alert_type="Counterparty Concentration",
                    risk_level=RiskLevel.HIGH,
                    confidence_score=80,
                    description="High concentration of transactions with single counterparty",
                    evidence=evidence,
                    timestamp=datetime.now(),
                    amount_involved=total_amount_by_counterparty.iloc[0]
                ))
        
        return alerts
    
    def detect_cash_intensive_patterns(self, df: pd.DataFrame, account_id: str) -> List[Alert]:
        """
        Detect patterns suggesting cash-intensive operations
        """
        alerts = []
        
        if 'transaction_type' not in df.columns:
            return alerts
        
        # Check for high percentage of cash transactions
        cash_transactions = df[df['transaction_type'].str.contains('cash|atm|withdrawal', case=False, na=False)]
        
        if len(cash_transactions) > 0:
            cash_percentage = len(cash_transactions) / len(df)
            cash_amount_percentage = cash_transactions['amount'].sum() / df['amount'].sum()
            
            if cash_percentage > 0.3 or cash_amount_percentage > 0.4:  # High cash activity
                evidence = [
                    f"Cash transactions: {cash_percentage:.2%} by count, {cash_amount_percentage:.2%} by amount",
                    f"Total cash amount: ${cash_transactions['amount'].sum():,.2f}"
                ]
                
                risk_level = RiskLevel.HIGH if cash_amount_percentage > 0.6 else RiskLevel.MEDIUM
                
                alerts.append(Alert(
                    account_id=account_id,
                    alert_type="High Cash Activity",
                    risk_level=risk_level,
                    confidence_score=75,
                    description="Unusually high level of cash transactions",
                    evidence=evidence,
                    timestamp=datetime.now(),
                    amount_involved=cash_transactions['amount'].sum()
                ))
        
        return alerts
    
    def detect_layering_patterns(self, df: pd.DataFrame, account_id: str) -> List[Alert]:
        """
        Detect potential money laundering layering patterns
        """
        alerts = []
        
        # Look for rapid in-out patterns (same day deposits and withdrawals)
        if 'date' not in df.columns or 'transaction_type' not in df.columns:
            return alerts
        
        df['date'] = pd.to_datetime(df['date'])
        daily_activity = df.groupby([df['date'].dt.date, 'transaction_type'])['amount'].sum().unstack(fill_value=0)
        
        if 'deposit' in daily_activity.columns and 'withdrawal' in daily_activity.columns:
            same_day_activity = daily_activity[(daily_activity['deposit'] > 0) & (daily_activity['withdrawal'] > 0)]
            
            if len(same_day_activity) > len(daily_activity) * 0.3:  # More than 30% of days have both
                evidence = [
                    f"{len(same_day_activity)} days with both deposits and withdrawals",
                    f"Potential layering pattern detected"
                ]
                
                alerts.append(Alert(
                    account_id=account_id,
                    alert_type="Layering Pattern",
                    risk_level=RiskLevel.HIGH,
                    confidence_score=85,
                    description="Rapid deposit and withdrawal patterns suggest potential layering",
                    evidence=evidence,
                    timestamp=datetime.now()
                ))
        
        return alerts
    
    def prioritize_alerts(self, alerts: List[Alert]) -> List[Alert]:
        """
        Prioritize and score alerts based on risk level and confidence
        """
        # Sort by risk level (descending) then confidence score (descending)
        return sorted(alerts, key=lambda x: (x.risk_level.value, x.confidence_score), reverse=True)
    
    def generate_report(self, alerts: List[Alert], account_id: str) -> str:
        """
        Generate a comprehensive report of findings
        """
        report = f"SLUSH FUND DETECTION REPORT\n"
        report += f"{'='*50}\n"
        report += f"Account ID: {account_id}\n"
        report += f"Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        report += f"Total Alerts: {len(alerts)}\n\n"
        
        if not alerts:
            report += "No suspicious patterns detected.\n"
            return report
        
        # Group by risk level
        risk_groups = {}
        for alert in alerts:
            if alert.risk_level not in risk_groups:
                risk_groups[alert.risk_level] = []
            risk_groups[alert.risk_level].append(alert)
        
        for risk_level in [RiskLevel.CRITICAL, RiskLevel.HIGH, RiskLevel.MEDIUM, RiskLevel.LOW]:
            if risk_level in risk_groups:
                report += f"\n{risk_level.name} RISK ALERTS ({len(risk_groups[risk_level])})\n"
                report += f"{'-'*30}\n"
                
                for alert in risk_groups[risk_level]:
                    report += f"\nAlert Type: {alert.alert_type}\n"
                    report += f"Confidence Score: {alert.confidence_score:.1f}%\n"
                    report += f"Description: {alert.description}\n"
                    if alert.amount_involved > 0:
                        report += f"Amount Involved: ${alert.amount_involved:,.2f}\n"
                    report += "Evidence:\n"
                    for evidence in alert.evidence:
                        report += f"  • {evidence}\n"
                    report += "\n"
        
        return report

# Example usage and testing
def create_sample_data() -> pd.DataFrame:
    """
    Create sample transaction data for testing
    """
    np.random.seed(42)
    
    dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='D')
    sample_dates = np.random.choice(dates, size=200)
    
    # Create suspicious patterns intentionally
    suspicious_amounts = [9999, 4999, 2999] * 10  # Threshold avoidance
    normal_amounts = np.random.normal(2500, 1000, 170).tolist()
    round_amounts = [5000, 10000, 15000] * 10  # Round numbers
    
    all_amounts = suspicious_amounts + normal_amounts + round_amounts
    np.random.shuffle(all_amounts)
    
    descriptions = (['Consulting services', 'Miscellaneous expenses', 'General services'] * 30 + 
                   ['Equipment purchase', 'Office supplies', 'Travel expenses'] * 70)
    np.random.shuffle(descriptions)
    
    counterparties = (['ABC Consulting LLC'] * 50 + 
                     ['XYZ Services', 'Quick Solutions Inc', 'Business Partners'] * 50)
    np.random.shuffle(counterparties)
    
    transaction_types = (['deposit', 'withdrawal'] * 100)
    np.random.shuffle(transaction_types)
    
    return pd.DataFrame({
        'date': sample_dates,
        'amount': [abs(x) for x in all_amounts],
        'description': descriptions,
        'counterparty': counterparties,
        'transaction_type': transaction_types
    })

# Example implementation
if __name__ == "__main__":
    # Initialize detector
    detector = SlushFundDetector()
    
    # Create sample data
    sample_transactions = create_sample_data()
    sample_account_info = {
        'account_id': 'ACC-12345',
        'account_type': 'Business Checking',
        'customer_id': 'CUST-67890'
    }
    
    # Run analysis
    print("Running slush fund detection analysis...")
    alerts = detector.analyze_account(sample_transactions, sample_account_info)
    
    # Generate report
    report = detector.generate_report(alerts, sample_account_info['account_id'])
    print(report)
    
    # Summary statistics
    print(f"\nSUMMARY STATISTICS")
    print(f"Total transactions analyzed: {len(sample_transactions)}")
    print(f"Total alerts generated: {len(alerts)}")
    print(f"High-risk alerts: {sum(1 for alert in alerts if alert.risk_level == RiskLevel.HIGH)}")
    print(f"Critical alerts: {sum(1 for alert in alerts if alert.risk_level == RiskLevel.CRITICAL)}")
